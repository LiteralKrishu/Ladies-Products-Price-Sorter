from lxml import html
from .base_scraper import BaseScraper

class JiomartScraper(BaseScraper):
    PLATFORM = "jiomart"
    BASE_URL = "https://www.jiomart.com/search/{query}"
    
    @classmethod
    async def scrape_products(cls, query: str) -> List[dict]:
        url = cls.BASE_URL.format(query=query.replace(" ", "%20"))
        html_content = await cls._fetch_html(url)
        if not html_content:
            return []
            
        tree = html.fromstring(html_content)
        products = []
        
        for item in tree.xpath('//div[contains(@class, "jm-col-4") and contains(@class, "product-item")]'):
            try:
                title = cls._clean_text("".join(item.xpath('.//a[contains(@class, "category_name")]/text()')))
                
                price = cls._parse_price("".join(item.xpath('.//span[contains(@class, "price")]/text()')))
                original_price = cls._parse_price("".join(item.xpath('.//span[contains(@class, "price-old")]/text()')))
                
                if not title or not price:
                    continue
                    
                discount = None
                if original_price and original_price > price:
                    discount = f"{round((1 - price/original_price)*100)}%"
                
                rating = None  # Jiomart doesn't show ratings in search results
                
                products.append({
                    "title": title,
                    "price": price,
                    "original_price": original_price if original_price > price else None,
                    "discount": discount,
                    "rating": rating,
                    "platform": cls.PLATFORM,
                    "image_url": item.xpath('.//img[contains(@class, "product-image")]/@src')[0],
                    "product_link": "https://www.jiomart.com" + item.xpath('.//a[contains(@class, "category_name")]/@href')[0],
                    "in_stock": not bool(item.xpath('.//div[contains(text(), "Out of Stock")]'))
                })
            except Exception as e:
                logger.error(f"Error parsing Jiomart product: {str(e)}")
                continue
                
        return products