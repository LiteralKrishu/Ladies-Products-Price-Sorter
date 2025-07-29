from lxml import html
from .base_scraper import BaseScraper

class AmazonScraper(BaseScraper):
    PLATFORM = "amazon"
    BASE_URL = "https://www.amazon.in/s?k={query}"
    
    @classmethod
    async def scrape_products(cls, query: str) -> List[dict]:
        url = cls.BASE_URL.format(query=query.replace(" ", "+"))
        html_content = await cls._fetch_html(url)
        if not html_content:
            return []
            
        tree = html.fromstring(html_content)
        products = []
        
        for item in tree.xpath('//div[contains(@data-component-type, "s-search-result")]'):
            try:
                title = cls._clean_text("".join(item.xpath('.//span[@class="a-size-medium a-color-base a-text-normal"]/text()')))
                price = cls._parse_price("".join(item.xpath('.//span[@class="a-price-whole"]/text()')))
                original_price = cls._parse_price("".join(item.xpath('.//span[@class="a-price a-text-price"]/span[2]/text()')))
                
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
                    "rating": float("".join(item.xpath('.//span[@class="a-icon-alt"]/text()')).split()[0]),
                    "platform": cls.PLATFORM,
                    "image_url": item.xpath('.//img[@class="s-image"]/@src')[0],
                    "product_link": "https://amazon.in" + item.xpath('.//a[@class="a-link-normal s-no-outline"]/@href')[0],
                    "in_stock": bool(item.xpath('.//span[contains(text(), "In Stock")]'))
                })
            except Exception as e:
                logger.error(f"Error parsing Amazon product: {str(e)}")
                continue
                
        return products