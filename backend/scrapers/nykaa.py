from core.scraper_base import ScraperBase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class NykaaScraper(ScraperBase):
    def scrape(self, query: str):
        search_query = query.replace(" ", "%20")
        url = f"https://www.nykaa.com/search/result/?q={search_query}&root=search&searchType=Manual"

        try:
            self._init_driver_with_retries(url)

            WebDriverWait(self.driver, 15).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.css-43m2vm"))
            )
            product_cards = self.driver.find_elements(By.CSS_SELECTOR, "div.css-43m2vm")

            results = []
            for card in product_cards[:10]:
                try:
                    title = self.extract_element(card, "div.css-xrzmfa")
                    price = self.extract_element(card, "span.css-111z9ua")

                    discount = self.extract_element(card, "span.css-1jczs19", optional=True)
                    rating = self.extract_element(card, "span.css-1b232jc", optional=True)

                    image_url = self.extract_attribute(
                        card, "img.css-8atqhb", "src", optional=True
                    ) or self.extract_attribute(
                        card, "img.css-8atqhb", "srcset", optional=True
                    )

                    product_link = self.extract_attribute(
                        card, "a", "href", optional=True
                    )

                    results.append({
                        "title": title,
                        "price": price,
                        "discount": discount,
                        "rating": rating,
                        "availability": "In Stock",
                        "delivery_time": "",
                        "image_url": image_url,
                        "product_link": product_link,
                    })

                except Exception:
                    continue

            self.cleanup(success=True)
            return results

        except Exception as e:
            print(f"[ERROR] Nykaa scraper failed: {e}")
            self.cleanup(success=False)
            return []
