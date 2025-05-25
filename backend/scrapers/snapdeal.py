from core.scraper_base import ScraperBase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SnapdealScraper(ScraperBase):
    def scrape(self, query: str):
        search_query = query.replace(" ", "%20")
        url = (
            f"https://www.snapdeal.com/search?keyword={search_query}"
            "&santizedKeyword=&catId=0&categoryId=0&suggested=true"
        )

        try:
            self._init_driver_with_retries(url)

            WebDriverWait(self.driver, 15).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.product-tuple-description"))
            )
            product_cards = self.driver.find_elements(By.CSS_SELECTOR, "div.product-tuple-description")

            results = []
            for card in product_cards[:10]:
                try:
                    title = self.extract_element(card, "p.product-title")
                    price = self.extract_element(card, "span.lfloat.product-price")
                    discount = self.extract_element(card, "span.product-discount", optional=True)

                    # Rating parsing from style attribute
                    rating = ""
                    try:
                        style = self.extract_attribute(card, "div.filled-stars", "style", optional=True)
                        if style and "width" in style:
                            pct = int(style.split(":")[1].replace("%;", "").strip())
                            rating = f"{round((pct / 100) * 5, 1)}"
                    except Exception:
                        pass

                    # Image from ancestor card
                    image_url = ""
                    try:
                        parent_card = card.find_element(By.XPATH, "./ancestor::div[contains(@class, 'product-tuple')]")
                        image_url = self.extract_attribute(parent_card, "img.product-image", "src", optional=True)
                    except Exception:
                        pass

                    product_link = self.extract_attribute(card, "a.dp-widget-link", "href", optional=True)

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
            print(f"[ERROR] Snapdeal scraper failed: {e}")
            self.cleanup(success=False)
            return []
