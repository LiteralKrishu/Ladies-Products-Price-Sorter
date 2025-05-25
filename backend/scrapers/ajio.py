from core.scraper_base import ScraperBase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AjioScraper(ScraperBase):
    def scrape(self, query: str):
        search_query = query.replace(" ", "%20")
        url = f"https://www.ajio.com/search/?text={search_query}"

        try:
            self._init_driver_with_retries(url)

            wait = WebDriverWait(self.driver, 15)
            product_cards = wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div.item")
            ))

            results = []
            for card in product_cards[:10]:
                try:
                    title = self.extract_element(card, "div.nameCls")
                    price = self.extract_element(card, "div.price span")

                    discount_raw = self.extract_element(card, "span.discount", optional=True)
                    discount = self.parse_discount(discount_raw)

                    rating_raw = self.extract_element(card, "span.rating", optional=True)
                    rating = self.parse_rating(rating_raw)

                    delivery = self.extract_element(card, "span.days", optional=True)
                    availability = "In Stock"

                    image_url = self.extract_attribute(card, "img", "src", optional=True) or \
                                self.extract_attribute(card, "img", "data-src", optional=True)

                    product_link = self.extract_attribute(card, "a", "href", optional=True)
                    if product_link and not product_link.startswith("http"):
                        product_link = f"https://www.ajio.com{product_link}"

                    results.append({
                        "title": title,
                        "price": price,
                        "discount": discount,
                        "rating": rating,
                        "delivery_time": delivery,
                        "availability": availability,
                        "image_url": image_url,
                        "product_link": product_link,
                    })

                except Exception:
                    continue  # Skip malformed entries

            self.cleanup(success=True)
            return results

        except Exception as e:
            print(f"[ERROR] Ajio scraper failed: {e}")
            self.cleanup(success=False)
            return []
