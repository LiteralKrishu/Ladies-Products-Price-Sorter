from lxml import html
from .base_scraper import BaseScraper

class SnapdealScraper(BaseScraper):
    PLATFORM = "snapdeal"
    BASE_URL = "https://www.snapdeal.com/search?keyword={query}"
    
    @classmethod
    async def scrape_products(cls, query: str) -> List[dict]:
        url = cls.BASE_URL.format(query=query.replace(" ", "%20"))
        html_content = await cls._fetch_html(url)
        if not html_content:
            return []
            
        tree = html.fromstring(html_content)
        products = []
        
        for item in tree.xpath('//div[contains(@class, "product-tuple-listing")]'):
            try:
                title = cls._clean_text("".join(item.xpath('.//p[contains(@class, "product-title")]/text()')))
                
                price = cls._parse_price("".join(item.xpath('.//span[contains(@class, "product-price")]/text()')))
                original_price = cls._parse_price("".join(item.xpath('.//span[contains(@class, "product-desc-price")]/text()')))
                
                if not title or not price:
                    continue
                    
                discount = None
                if original_price and original_price > price:
                    discount = f"{round((1 - price/original_price)*100)}%"
                
                rating = float(item.xpath('.//div[contains(@class, "filled-stars")]/@style')[0].split(":")[1].replace("%", ""))/20 if item.xpath('.//div[contains(@class, "filled-stars")]/@style') else None
                
                products.append({
                    "title": title,
                    "price": price,
                    "original_price": original_price if original_price > price else None,
                    "discount": discount,
                    "rating": rating,
                    "platform": cls.PLATFORM,
                    "image_url": item.xpath('.//img[contains(@class, "product-image")]/@src')[0],
                    "product_link": item.xpath('.//a[contains(@class, "dp-widget-link")]/@href')[0],
                    "in_stock": not bool(item.xpath('.//div[contains(text(), "Sold Out")]'))
                })
            except Exception as e:
                logger.error(f"Error parsing Snapdeal product: {str(e)}")
                continue
                
        return products