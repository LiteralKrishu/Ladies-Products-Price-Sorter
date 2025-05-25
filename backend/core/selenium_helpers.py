import time
from functools import wraps
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core.config import MAX_RETRIES, RETRY_DELAY, RETRY_BACKOFF, SELENIUM_WAIT_TIMEOUT

def retry_on_exception(
    exceptions, tries=MAX_RETRIES, delay=RETRY_DELAY, backoff=RETRY_BACKOFF
):
    """
    Decorator for retrying a function with exponential backoff on given exceptions.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            _tries, _delay = tries, delay
            while _tries > 1:
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    time.sleep(_delay)
                    _tries -= 1
                    _delay *= backoff
            return func(*args, **kwargs)
        return wrapper
    return decorator

def wait_for_element(driver, by, locator, timeout=SELENIUM_WAIT_TIMEOUT):
    """
    Wait for an element to be present and visible.
    """
    try:
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.visibility_of_element_located((by, locator)))
        return element
    except TimeoutException:
        return None
