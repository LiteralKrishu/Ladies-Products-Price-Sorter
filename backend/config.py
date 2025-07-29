import os
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()

class Config:
    # Proxy Configuration
    PROXY_ENABLED = os.getenv("PROXY_ENABLED", "true").lower() == "true"
    PROXY_LIST = [
        {"http": proxy.strip(), "https": proxy.strip()} 
        for proxy in os.getenv("PROXY_LIST", "").split(",") 
        if proxy.strip()
    ]
    
    # Scraping Settings
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "15"))
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
    ROTATE_USER_AGENT = os.getenv("ROTATE_USER_AGENT", "true").lower() == "true"
    
    # Platform Toggles
    PLATFORMS = {
        "amazon": os.getenv("ENABLE_AMAZON", "true").lower() == "true",
        "flipkart": os.getenv("ENABLE_FLIPKART", "true").lower() == "true",
        "myntra": os.getenv("ENABLE_MYNTRA", "true").lower() == "true",
        "nykaa": os.getenv("ENABLE_NYKAA", "true").lower() == "true",
        "ajio": os.getenv("ENABLE_AJIO", "true").lower() == "true",
        "jiomart": os.getenv("ENABLE_JIOMART", "true").lower() == "true",
        "snapdeal": os.getenv("ENABLE_SNAPDEAL", "true").lower() == "true",
    }
    
    @staticmethod
    def get_active_platforms() -> List[str]:
        return [platform for platform, enabled in Config.PLATFORMS.items() if enabled]