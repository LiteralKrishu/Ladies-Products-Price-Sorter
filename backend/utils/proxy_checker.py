import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from backend.utils.proxy_manager import ProxyManager
from backend.config import Config

async def main():
    print("=== Proxy Checker ===")
    
    manager = ProxyManager(Config.PROXY_LIST)
    print(f"Loaded {len(manager.proxies)} proxies")
    
    print("\nValidating proxies...")
    for proxy in manager.proxies:
        is_valid = await manager.validate_proxy(proxy)
        status = "✓" if is_valid else "✗"
        print(f"{status} {proxy['http']}")
    
    print("\nSummary:")
    print(f"Good proxies: {len(manager.good_proxies)}")
    print(f"Bad proxies: {len(manager.bad_proxies)}")

if __name__ == "__main__":
    asyncio.run(main())