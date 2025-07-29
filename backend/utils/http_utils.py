import httpx
from fake_useragent import UserAgent
from typing import Optional, Dict
from ..config import Config
from .proxy_manager import proxy_manager
import logging

logger = logging.getLogger(__name__)
ua = UserAgent()

async def make_request(
    url: str,
    method: str = "GET",
    headers: Optional[Dict] = None,
    params: Optional[Dict] = None,
    retries: int = Config.MAX_RETRIES
) -> Optional[httpx.Response]:
    """Generic HTTP request maker with proxy rotation and retries"""
    base_headers = {
        "User-Agent": ua.random if Config.ROTATE_USER_AGENT else "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9",
    }
    if headers:
        base_headers.update(headers)
    
    for attempt in range(retries):
        proxy = proxy_manager.get_next_proxy() if Config.PROXY_ENABLED else None
        try:
            async with httpx.AsyncClient(
                proxies=proxy,
                timeout=Config.REQUEST_TIMEOUT,
                follow_redirects=True
            ) as client:
                response = await client.request(
                    method,
                    url,
                    headers=base_headers,
                    params=params
                )
                
                if response.status_code == 200:
                    return response
                elif response.status_code in [403, 429]:
                    if proxy:
                        proxy_manager.mark_bad(proxy)
                    logger.warning(f"Blocked (Attempt {attempt + 1}) - Status {response.status_code}")
                else:
                    logger.warning(f"Status {response.status_code} for {url}")
        except Exception as e:
            if proxy:
                proxy_manager.mark_bad(proxy)
            logger.error(f"Request failed: {str(e)}")
    
    logger.error(f"Max retries ({retries}) exceeded for {url}")
    return None