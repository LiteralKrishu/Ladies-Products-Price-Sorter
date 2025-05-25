from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import asyncio

from scrapers import (
    FlipkartScraper, AmazonScraper, AjioScraper,
    JioMartScraper, MyntraScraper, NykaaScraper, SnapdealScraper
)
from utils.cache import get_cache, set_cache
from utils.price_utils import (
    normalize_price, normalize_discount,
    normalize_rating, normalize_delivery_time
)

app = FastAPI(title="Ladies Product Price Sorter API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SCRAPER_CLASS_MAP = {
    "flipkart": FlipkartScraper,
    "amazon": AmazonScraper,
    "ajio": AjioScraper,
    "jiomart": JioMartScraper,
    "myntra": MyntraScraper,
    "nykaa": NykaaScraper,
    "snapdeal": SnapdealScraper,
}

async def run_scraper(scraper_class, query: str):
    scraper = scraper_class()
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, scraper.scrape, query)

# Single platform scrape
@app.get("/scrape")
async def scrape(
    platform: str = Query(...),
    query: str = Query(...),
):
    platform = platform.lower()
    if platform not in SCRAPER_CLASS_MAP:
        raise HTTPException(status_code=400, detail=f"Unsupported platform: {platform}")

    try:
        results = await run_scraper(SCRAPER_CLASS_MAP[platform], query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")

    return {"platform": platform, "query": query, "results": results}

# Aggregated scrape
@app.get("/aggregate")
async def aggregate_prices(
    q: str = Query(...),
    sort_by: Optional[str] = Query("relevance", pattern="^(price|title|relevance)$"),
    order: Optional[str] = Query("asc", pattern="^(asc|desc)$"),
    min_price: Optional[int] = Query(None, ge=0),
    max_price: Optional[int] = Query(None, ge=0),
    min_discount: int = Query(0, ge=0, le=100),
    min_rating: float = Query(0.0, ge=0.0, le=5.0),
    max_delivery_days: int = Query(999, ge=1),
    availability: Optional[str] = Query(None),
    platforms: Optional[str] = Query(None),
):
    cache_key = f"aggregate:{q}:{sort_by}:{order}:{min_price}:{max_price}:{min_discount}:{min_rating}:{max_delivery_days}:{availability}:{platforms}"
    cached = get_cache(cache_key)
    if cached:
        return {"query": q, "results": cached, "cached": True}

    if platforms:
        requested_platforms = set(p.strip().lower() for p in platforms.split(","))
        invalid = requested_platforms - set(SCRAPER_CLASS_MAP.keys())
        if invalid:
            raise HTTPException(status_code=400, detail=f"Unsupported platforms: {', '.join(invalid)}")
    else:
        requested_platforms = set(SCRAPER_CLASS_MAP.keys())

    tasks = [run_scraper(SCRAPER_CLASS_MAP[name], q) for name in requested_platforms]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    aggregated = []
    for result in results:
        if isinstance(result, Exception):
            continue
        for item in result:
            if "error" in item:
                continue

            price_int = normalize_price(item.get("price", ""))
            if (min_price is not None and price_int < min_price) or (
                max_price is not None and price_int > max_price
            ):
                continue

            discount = normalize_discount(item.get("discount", ""))
            rating = normalize_rating(item.get("rating", ""))
            delivery = normalize_delivery_time(item.get("delivery_time", ""))
            avail = item.get("availability", "").lower()

            if discount < min_discount or rating < min_rating or delivery > max_delivery_days:
                continue
            if availability and availability.lower() != avail:
                continue

            item["price_int"] = price_int
            aggregated.append(item)

    if sort_by == "price":
        aggregated.sort(key=lambda x: x["price_int"], reverse=(order == "desc"))
    elif sort_by == "title":
        aggregated.sort(key=lambda x: x["title"].lower(), reverse=(order == "desc"))

    for item in aggregated:
        item.pop("price_int", None)

    set_cache(cache_key, aggregated, ttl=300)
    return {"query": q, "results": aggregated, "cached": False}
