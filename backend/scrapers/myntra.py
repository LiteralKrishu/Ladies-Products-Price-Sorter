from lxml import html
from .base_scraper import BaseScraper
import re

class MyntraScraper(BaseScraper):
    PLATFORM = "myntra"
    BASE_URL = "https://www.myntra.com/{query}"
    
    @classmethod
    async def scrape_products(cls, query: str) -> List[dict]:
        url = cls.BASE_URL.format(query=query.replace(" ", "-"))
        html_content = await cls._fetch_html(url)
        if not html_content:
            return []
            
        tree = html.fromstring(html_content)
        products = []
        
        for item in tree.xpath('//li[contains(@class, "product-base")]'):
            try:
                title = cls._clean_text("".join(item.xpath('.//h3[contains(@class, "product-brand")]/text()'))) + " " + \
                        cls._clean_text("".join(item.xpath('.//h4[contains(@class, "product-product")]/text()')))
                
                price = cls._parse_price("".join(item.xpath('.//div[contains(@class, "product-price")]//span/text()')))
                original_price = cls._parse_price("".join(item.xpath('.//span[contains(@class, "product-strike")]/text()')))
                
                if not title or not price:
                    continue
                    
                discount = None
                if original_price and original_price > price:
                    discount = f"{round((1 - price/original_price)*100)}%"
                
                rating_text = "".join(item.xpath('.//div[contains(@class, "product-ratingsContainer")]/text()'))
                rating = float(rating_text) if rating_text else None
                
                products.append({
                    "title": title,
                    "price": price,
                    "original_price": original_price if original_price > price else None,
                    "discount": discount,
                    "rating": rating,
                    "platform": cls.PLATFORM,
                    "image_url": item.xpath('.//img[contains(@class, "img-responsive")]/@src')[0],
                    "product_link": "https://www.myntra.com" + item.xpath('./a/@href')[0],
                    "in_stock": True  # Myntra typically shows only available items
                })
            except Exception as e:
                logger.error(f"Error parsing Myntra product: {str(e)}")
                continue
                
        return products