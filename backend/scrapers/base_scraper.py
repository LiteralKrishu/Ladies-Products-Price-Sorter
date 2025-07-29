import httpx
import logging
from typing import List, Optional
from fake_useragent import UserAgent
from ..utils.proxy_manager import proxy_manager
from ..config import Config

logger = logging.getLogger(__name__)
ua = UserAgent()

class BaseScraper:
    PLATFORM = None
    BASE_URL = None
    
    @classmethod
    async def _fetch_html(cls, url: str) -> Optional[str]:
        headers = {
            "User-Agent": ua.random if Config.ROTATE_USER_AGENT else "Mozilla/5.0",
            "Accept-Language": "en-US,en;q=0.9",
        }
        
        for attempt in range(Config.MAX_RETRIES):
            proxy = None
            if Config.PROXY_ENABLED:
                proxy = proxy_manager.get_next_proxy()
            
            try:
                async with httpx.AsyncClient(
                    proxies=proxy,
                    headers=headers,
                    timeout=Config.REQUEST_TIMEOUT,
                    follow_redirects=True
                ) as client:
                    response = await client.get(url)
                    
                    if response.status_code == 200:
                        return response.text
                    elif response.status_code in [403, 429]:
                        if proxy:
                            proxy_manager.mark_bad(proxy)
                        logger.warning(f"Blocked by {cls.PLATFORM} (Attempt {attempt + 1})")
                    else:
                        logger.warning(f"Status {response.status_code} from {cls.PLATFORM}")
            except Exception as e:
                if proxy:
                    proxy_manager.mark_bad(proxy)
                logger.error(f"Error fetching {url}: {str(e)}")
        
        logger.error(f"Failed to fetch {url} after {Config.MAX_RETRIES} attempts")
        return None
    
    @classmethod
    def _clean_text(cls, text: str) -> str:
        return " ".join(text.replace("\n", " ").replace("\t", " ").strip().split())
    
    @classmethod
    def _parse_price(cls, price_str: str) -> float:
        try:
            return float("".join(c for c in price_str if c.isdigit() or c == "."))
        except:
            return 0.0
    
    @classmethod
    async def scrape_products(cls, query: str) -> List[dict]:
        raise NotImplementedError