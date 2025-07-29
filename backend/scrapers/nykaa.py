from lxml import html
from .base_scraper import BaseScraper

class NykaaScraper(BaseScraper):
    PLATFORM = "nykaa"
    BASE_URL = "https://www.nykaa.com/search/result/?q={query}"
    
    @classmethod
    async def scrape_products(cls, query: str) -> List[dict]:
        url = cls.BASE_URL.format(query=query.replace(" ", "%20"))
        html_content = await cls._fetch_html(url)
        if not html_content:
            return []
            
        tree = html.fromstring(html_content)
        products = []
        
        for item in tree.xpath('//div[contains(@class, "product-card")]'):
            try:
                title = cls._clean_text("".join(item.xpath('.//h2[contains(@class, "product-name")]/text()')))
                
                price = cls._parse_price("".join(item.xpath('.//span[contains(@class, "post-discount")]/text()')))
                original_price = cls._parse_price("".join(item.xpath('.//span[contains(@class, "post-card")]/span[@class="strike-through"]/text()')))
                
                if not title or not price:
                    continue
                    
                discount = None
                if original_price and original_price > price:
                    discount = f"{round((1 - price/original_price)*100)}%"
                
                rating = float(item.xpath('.//div[contains(@class, "product-rating")]/span/text()')[0]) if item.xpath('.//div[contains(@class, "product-rating")]/span/text()') else None
                
                products.append({
                    "title": title,
                    "price": price,
                    "original_price": original_price if original_price > price else None,
                    "discount": discount,
                    "rating": rating,
                    "platform": cls.PLATFORM,
                    "image_url": item.xpath('.//img[contains(@class, "product-image")]/@src')[0],
                    "product_link": "https://www.nykaa.com" + item.xpath('.//a[contains(@class, "product-card")]/@href')[0],
                    "in_stock": bool(item.xpath('.//button[contains(text(), "Add to Bag")]'))
                })
            except Exception as e:
                logger.error(f"Error parsing Nykaa product: {str(e)}")
                continue
                
        return products