from lxml import html
from .base_scraper import BaseScraper

class AjioScraper(BaseScraper):
    PLATFORM = "ajio"
    BASE_URL = "https://www.ajio.com/search/?text={query}"
    
    @classmethod
    async def scrape_products(cls, query: str) -> List[dict]:
        url = cls.BASE_URL.format(query=query.replace(" ", "%20"))
        html_content = await cls._fetch_html(url)
        if not html_content:
            return []
            
        tree = html.fromstring(html_content)
        products = []
        
        for item in tree.xpath('//div[contains(@class, "item rilrtl-products-list__item")]'):
            try:
                title = cls._clean_text("".join(item.xpath('.//div[contains(@class, "nameCls")]/text()')))
                
                price = cls._parse_price("".join(item.xpath('.//span[contains(@class, "price")]/text()')))
                original_price = cls._parse_price("".join(item.xpath('.//span[contains(@class, "orginal-price")]/text()')))
                
                if not title or not price:
                    continue
                    
                discount = None
                if original_price and original_price > price:
                    discount = f"{round((1 - price/original_price)*100)}%"
                
                rating = None  # Ajio doesn't show ratings in search results
                
                products.append({
                    "title": title,
                    "price": price,
                    "original_price": original_price if original_price > price else None,
                    "discount": discount,
                    "rating": rating,
                    "platform": cls.PLATFORM,
                    "image_url": item.xpath('.//img[contains(@class, "rilrtl-lazy-img")]/@src')[0],
                    "product_link": "https://www.ajio.com" + item.xpath('.//a[contains(@class, "rilrtl-products-list__link")]/@href')[0],
                    "in_stock": not bool(item.xpath('.//span[contains(text(), "SOLD OUT")]'))
                })
            except Exception as e:
                logger.error(f"Error parsing Ajio product: {str(e)}")
                continue
                
        return products