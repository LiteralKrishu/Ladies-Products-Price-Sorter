from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By

from core.proxy_manager import get_weighted_proxy, report_proxy_result
from core.selenium_helpers import retry_on_exception
from core.config import MAX_RETRIES, SELENIUM_HEADLESS, SELENIUM_PAGE_LOAD_TIMEOUT, RETRY_DELAY, RETRY_BACKOFF

class ScraperBase:
    MAX_RETRIES = MAX_RETRIES
    HEADLESS = SELENIUM_HEADLESS

    def __init__(self):
        self.driver = None
        self.proxy = None  # Track proxy used in current session

    def _configure_driver(self, proxy=None):
        chrome_options = Options()
        if self.HEADLESS:
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_experimental_option("prefs", {
                "profile.managed_default_content_settings.images": 2,
                "profile.managed_default_content_settings.stylesheets": 2,
            })

        if proxy:
            chrome_options.add_argument(f'--proxy-server={proxy}')
            print(f"[INFO] Using proxy: {proxy}")

        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        return webdriver.Chrome(options=chrome_options)

    def _detect_captcha(self):
        title = self.driver.title.lower()
        html = self.driver.page_source.lower()
        return "captcha" in title or "verify you are human" in html

    @retry_on_exception(
        exceptions=(TimeoutException, WebDriverException),
        tries=MAX_RETRIES,
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
    )
    def _init_driver_with_retries(self, target_url):
        self.proxy = get_weighted_proxy()
        self.driver = self._configure_driver(self.proxy)
        self.driver.set_page_load_timeout(SELENIUM_PAGE_LOAD_TIMEOUT)

        self.driver.get(target_url)

        if self._detect_captcha():
            print("[WARNING] CAPTCHA detected. Retrying...")
            self.driver.quit()
            raise WebDriverException("CAPTCHA triggered")

    def scrape(self, query: str):
        raise NotImplementedError("Subclasses must implement scrape() method.")

    def cleanup(self, success=True):
        if self.driver:
            self.driver.quit()
        if self.proxy:
            report_proxy_result(self.proxy, success)
            self.proxy = None

    def extract_element(self, card, selector: str, optional: bool = False) -> str:
        try:
            return card.find_element(By.CSS_SELECTOR, selector).text.strip()
        except Exception:
            return "" if optional else None

    def extract_attribute(self, card, selector: str, attr: str, optional: bool = False) -> str:
        try:
            return card.find_element(By.CSS_SELECTOR, selector).get_attribute(attr)
        except Exception:
            return "" if optional else None

    def parse_discount(self, text: str) -> str:
        if text:
            return text.strip().replace("OFF", "off")
        return ""

    def parse_rating(self, text: str) -> str:
        if text:
            for token in text.split():
                if token.replace(".", "").isdigit():
                    return token
        return ""
