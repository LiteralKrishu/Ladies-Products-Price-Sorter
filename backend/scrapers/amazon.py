from core.scraper_base import ScraperBase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AmazonScraper(ScraperBase):
    def scrape(self, query: str):
        search_query = query.replace(" ", "+")
        url = f"https://www.amazon.in/s?k={search_query}"

        try:
            self._init_driver_with_retries(url)

            wait = WebDriverWait(self.driver, 15)
            product_cards = wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div.s-result-item[data-component-type='s-search-result']")
            ))

            results = []
            for card in product_cards[:10]:
                try:
                    title = self.extract_element(card, "span.a-text-normal")

                    price_whole = self.extract_element(card, "span.a-price-whole", optional=True)
                    price_fraction = self.extract_element(card, "span.a-price-fraction", optional=True)
                    price = f"₹{price_whole}{price_fraction}" if price_whole else ""

                    discount_raw = self.extract_element(card, "span.a-letter-space + span", optional=True)
                    discount = self.parse_discount(discount_raw)

                    rating_raw = self.extract_element(card, "span.a-icon-alt", optional=True)
                    rating = self.parse_rating(rating_raw)

                    delivery = self.extract_element(card, "span.a-color-base.a-text-bold", optional=True)
                    availability = "In Stock" if "out of stock" not in card.text.lower() else "Out of Stock"

                    image_url = self.extract_attribute(card, "img.s-image", "src", optional=True)
                    product_link = self.extract_attribute(card, "a.a-link-normal.s-no-outline", "href", optional=True)

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
                    continue

            self.cleanup(success=True)
            return results

        except Exception as e:
            print(f"[ERROR] Amazon scraper failed: {e}")
            self.cleanup(success=False)
            return []
