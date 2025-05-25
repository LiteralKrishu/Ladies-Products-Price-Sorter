from core.scraper_base import ScraperBase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MyntraScraper(ScraperBase):
    def scrape(self, query: str):
        search_query = query.replace(" ", "%20")
        url = f"https://www.myntra.com/{search_query}"

        try:
            self._init_driver_with_retries(url)

            WebDriverWait(self.driver, 15).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.product-base"))
            )
            product_cards = self.driver.find_elements(By.CSS_SELECTOR, "li.product-base")

            results = []
            for card in product_cards[:10]:
                try:
                    brand = self.extract_element(card, "h3.product-brand")
                    name = self.extract_element(card, "h4.product-product")
                    full_title = f"{brand} {name}"

                    price = self.extract_element(card, "div.product-price span")

                    discount = self.extract_element(
                        card, "span.product-discountPercentage", optional=True
                    )

                    image_url = self.extract_attribute(
                        card, "img.product-image", "src", optional=True
                    ) or self.extract_attribute(
                        card, "img.product-image", "srcset", optional=True
                    )

                    product_link = self.extract_attribute(
                        card, "a", "href", optional=True
                    )

                    results.append({
                        "title": full_title,
                        "price": price,
                        "discount": discount,
                        "rating": "",  # Ratings not shown on listings
                        "availability": "In Stock",
                        "delivery_time": "",  # Not visible on listing page
                        "image_url": image_url,
                        "product_link": product_link,
                    })

                except Exception:
                    continue

            self.cleanup(success=True)
            return results

        except Exception as e:
            print(f"[ERROR] Myntra scraper failed: {e}")
            self.cleanup(success=False)
            return []
