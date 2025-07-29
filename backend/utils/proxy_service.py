import asyncio
import logging
from .proxy_manager import proxy_manager
from ..config import Config

logger = logging.getLogger(__name__)

async def validate_proxy(proxy: Dict[str, str]) -> bool:
    """Validate a single proxy"""
    test_urls = [
        "https://httpbin.org/ip",
        "https://api.ipify.org?format=json",
        "https://www.amazon.com"
    ]
    
    try:
        async with httpx.AsyncClient(
            proxies=proxy,
            timeout=Config.REQUEST_TIMEOUT
        ) as client:
            for url in test_urls:
                response = await client.get(url)
                if response.status_code != 200:
                    return False
            return True
    except Exception:
        return False

async def periodic_proxy_validation(interval: int = 600):
    """Continuously validate and maintain proxy pool"""
    while True:
        logger.info("Starting proxy validation cycle")
        
        # Validate all good proxies
        validation_tasks = [
            validate_proxy(proxy) 
            for proxy in proxy_manager.good_proxies.copy()
        ]
        results = await asyncio.gather(*validation_tasks)
        
        # Mark failed proxies
        for proxy, is_valid in zip(proxy_manager.good_proxies.copy(), results):
            if not is_valid:
                proxy_manager.mark_bad(proxy)
        
        # Try to reactivate some bad proxies
        proxy_manager._reactivate_proxies()
        
        logger.info(
            f"Proxy status: {len(proxy_manager.good_proxies)} good, "
            f"{len(proxy_manager.bad_proxies)} bad"
        )
        await asyncio.sleep(interval)

def start_proxy_validator():
    """Start the proxy validation service"""
    asyncio.create_task(periodic_proxy_validation())