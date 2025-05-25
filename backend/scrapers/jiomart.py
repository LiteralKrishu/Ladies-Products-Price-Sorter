from core.scraper_base import ScraperBase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class JioMartScraper(ScraperBase):
    def scrape(self, query: str):
        search_query = query.replace(" ", "%20")
        url = f"https://www.jiomart.com/catalogsearch/result?q={search_query}"

        try:
            self._init_driver_with_retries(url)

            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.cat-item"))
            )

            product_cards = self.driver.find_elements(By.CSS_SELECTOR, "div.cat-item")

            results = []
            for card in product_cards[:10]:
                try:
                    title = self.extract_element(card, "span.clsgetname")
                    price = self.extract_element(card, "span.price", optional=True)

                    original_price = self.extract_element(card, "span.mrp", optional=True)
                    discount = ""
                    if price and original_price:
                        try:
                            p = float(price.replace('₹', '').replace(',', ''))
                            op = float(original_price.replace('₹', '').replace(',', ''))
                            discount_percent = round((1 - p / op) * 100)
                            discount = f"{discount_percent}% off" if discount_percent > 0 else ""
                        except Exception:
                            discount = ""

                    availability = "In Stock" if title else "Out of Stock"

                    image_url = self.extract_attribute(card, "img.cat-image", "src", optional=True)
                    product_link = self.extract_attribute(card, "a.cat-image", "href", optional=True)

                    results.append({
                        "title": title,
                        "price": price,
                        "discount": discount,
                        "rating": "",  # JioMart does not provide listing ratings
                        "availability": availability,
                        "delivery_time": "",  # Not visible up front
                        "image_url": image_url,
                        "product_link": product_link,
                    })

                except Exception:
                    continue

            self.cleanup(success=True)
            return results

        except Exception as e:
            print(f"[ERROR] JioMart scraper failed: {e}")
            self.cleanup(success=False)
            return []
