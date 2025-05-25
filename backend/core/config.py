# Proxy list for India-based proxies
PROXY_POOL = [
    "http://103.168.101.166:3128",
    "http://103.166.10.142:83",
    "http://103.168.94.143:83",
    "http://103.231.78.36:80",
    "http://103.138.75.234:84",
    "http://103.47.67.134:83",
    "http://103.145.37.202:84",
    "http://103.141.108.122:8080",
    "http://103.216.82.216:6666",
    "http://103.87.169.178:8080",
    "http://103.92.26.190:8080",
    "http://103.122.248.50:8080",
    "http://103.105.49.53:80",
    "http://103.159.46.2:83",
    "http://103.78.213.226:8080",
    "http://103.81.214.254:82",
]

# Retry configuration
MAX_RETRIES = 5
RETRY_DELAY = 2  # seconds
RETRY_BACKOFF = 2.0

# Selenium config
SELENIUM_HEADLESS = True
SELENIUM_PAGE_LOAD_TIMEOUT = 30  # seconds
SELENIUM_WAIT_TIMEOUT = 15  # seconds

# Cache TTL (seconds)
CACHE_TTL = 300

# Other constants
MAX_RESULTS_PER_SCRAPER = 10
