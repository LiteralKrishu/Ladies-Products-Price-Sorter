from lxml import html
from .base_scraper import BaseScraper

class FlipkartScraper(BaseScraper):
    PLATFORM = "flipkart"
    BASE_URL = "https://www.flipkart.com/search?q={query}"
    
    @classmethod
    async def scrape_products(cls, query: str) -> List[dict]:
        url = cls.BASE_URL.format(query=query.replace(" ", "%20"))
        html_content = await cls._fetch_html(url)
        if not html_content:
            return []
            
        tree = html.fromstring(html_content)
        products = []
        
        for item in tree.xpath('//div[contains(@class, "_1AtVbE")]'):
            try:
                title = cls._clean_text("".join(item.xpath('.//a[contains(@class, "IRpwTa") or contains(@class, "s1Q9rs")]/text()')))
                price = cls._parse_price("".join(item.xpath('.//div[contains(@class, "_30jeq3")]/text()')))
                original_price = cls._parse_price("".join(item.xpath('.//div[contains(@class, "_3I9_wc")]/text()')))
                
                if not title or not price:
                    continue
                    
                discount = None
                if original_price and original_price > price:
                    discount = f"{round((1 - price/original_price)*100)}%"
                
                products.append({
                    "title": title,
                    "price": price,
                    "original_price": original_price if original_price > price else None,
                    "discount": discount,
                    "rating": float(item.xpath('.//div[@class="_3LWZlK"]/text()')[0]) if item.xpath('.//div[@class="_3LWZlK"]/text()') else None,
                    "platform": cls.PLATFORM,
                    "image_url": item.xpath('.//img[@class="_396cs4"]/@src')[0],
                    "product_link": "https://flipkart.com" + item.xpath('.//a[contains(@class, "_1fQZEK") or contains(@class, "_2UzuFa")]/@href')[0],
                    "in_stock": bool(item.xpath('.//div[contains(text(), "Available")]'))
                })
            except Exception as e:
                logger.error(f"Error parsing Flipkart product: {str(e)}")
                continue
                
        return products