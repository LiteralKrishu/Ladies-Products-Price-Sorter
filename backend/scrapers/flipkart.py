from core.scraper_base import ScraperBase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class FlipkartScraper(ScraperBase):
    def scrape(self, query: str):
        search_query = query.replace(" ", "+")
        url = f"https://www.flipkart.com/search?q={search_query}"

        try:
            self._init_driver_with_retries(url)

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div._1YokD2._3Mn1Gg"))
            )

            # Close login popup if it appears
            try:
                close_btn = self.driver.find_element(By.CSS_SELECTOR, "button._2KpZ6l._2doB4z")
                close_btn.click()
            except Exception:
                pass

            product_cards = self.driver.find_elements(By.CSS_SELECTOR, "div._1AtVbE")

            results = []
            for card in product_cards:
                try:
                    title = self.extract_element(card, "div._4rR01T", optional=True) or \
                            self.extract_element(card, "a.IRpwTa", optional=True)
                    if not title:
                        continue

                    price = self.extract_element(card, "div._30jeq3", optional=True)
                    discount = self.extract_element(card, "div._3Ay6Sb span", optional=True)
                    rating_raw = self.extract_element(card, "div._3LWZlK", optional=True)
                    rating = self.parse_rating(rating_raw)

                    image_url = self.extract_attribute(card, "img._396cs4", "src", optional=True)
                    product_link = self.extract_attribute(card, "a._1fQZEK", "href", optional=True) or \
                                   self.extract_attribute(card, "a.IRpwTa", "href", optional=True)

                    results.append({
                        "title": title,
                        "price": price,
                        "discount": discount,
                        "rating": rating,
                        "availability": "In Stock" if title else "Out of Stock",
                        "delivery_time": "",  # Flipkart doesn't expose up-front
                        "image_url": image_url,
                        "product_link": product_link,
                    })

                except Exception:
                    continue

            self.cleanup(success=True)
            return results

        except Exception as e:
            print(f"[ERROR] Flipkart scraper failed: {e}")
            self.cleanup(success=False)
            return []
