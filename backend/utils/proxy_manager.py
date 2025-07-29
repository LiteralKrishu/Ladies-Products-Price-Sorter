import random
import logging
import httpx
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

class ProxyManager:
    def __init__(self, proxy_list: List[Dict[str, str]] = None):
        self.proxies = proxy_list or []
        self.good_proxies = self.proxies.copy()
        self.bad_proxies = []
        self.current_index = 0
        self.executor = ThreadPoolExecutor(max_workers=5)
        
    def add_proxy(self, proxy: Dict[str, str]):
        if proxy not in self.proxies:
            self.proxies.append(proxy)
            self.good_proxies.append(proxy)
            
    def mark_bad(self, proxy: Dict[str, str]):
        if proxy in self.good_proxies:
            self.good_proxies.remove(proxy)
            self.bad_proxies.append(proxy)
            logger.warning(f"Proxy marked bad: {proxy['http']}")
            
            # Reactivate some bad proxies if good pool is low
            if len(self.good_proxies) < max(3, len(self.proxies) // 3):
                self._reactivate_proxies()
    
    def _reactivate_proxies(self):
        reactivate_count = max(1, len(self.bad_proxies) // 3)
        for _ in range(reactivate_count):
            if self.bad_proxies:
                proxy = random.choice(self.bad_proxies)
                self.bad_proxies.remove(proxy)
                self.good_proxies.append(proxy)
                logger.info(f"Reactivated proxy: {proxy['http']}")
    
    def get_next_proxy(self) -> Optional[Dict[str, str]]:
        if not self.good_proxies:
            return None
        proxy = self.good_proxies[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.good_proxies)
        return proxy
    
    async def validate_proxy(self, proxy: Dict[str, str]) -> bool:
        test_urls = [
            "https://httpbin.org/ip",
            "https://api.ipify.org?format=json"
        ]
        try:
            async with httpx.AsyncClient(proxies=proxy, timeout=10.0) as client:
                for url in test_urls:
                    response = await client.get(url)
                    if response.status_code != 200:
                        return False
                return True
        except Exception as e:
            logger.debug(f"Proxy validation failed: {str(e)}")
            return False

# Initialize with configuration
proxy_manager = ProxyManager(Config.PROXY_LIST)