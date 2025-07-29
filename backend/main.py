from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Dict, Any
import asyncio
import logging
from .config import Config
from .models.product import Product
from .scrapers import (
    AmazonScraper,
    FlipkartScraper,
    MyntraScraper,
    NykaaScraper,
    AjioScraper,
    JiomartScraper,
    SnapdealScraper
)
from .utils.proxy_service import start_proxy_validator

app = FastAPI(
    title="Ladies Product Price Sorter API",
    description="Compare prices across Indian e-commerce platforms",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Platform mapping
PLATFORM_SCRAPERS = {
    "amazon": AmazonScraper,
    "flipkart": FlipkartScraper,
    "myntra": MyntraScraper,
    "nykaa": NykaaScraper,
    "ajio": AjioScraper,
    "jiomart": JiomartScraper,
    "snapdeal": SnapdealScraper
}

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_proxy_validator())

@app.get("/search", response_model=List[Product])
async def search_products(q: str, platforms: str = None):
    if not q or len(q) < 3:
        raise HTTPException(status_code=400, detail="Query too short")
    
    platform_list = platforms.split(",") if platforms else Config.get_active_platforms()
    valid_platforms = [p for p in platform_list if p in PLATFORM_SCRAPERS and Config.PLATFORMS.get(p, False)]
    
    if not valid_platforms:
        raise HTTPException(status_code=400, detail="No valid platforms specified")
    
    tasks = []
    for platform in valid_platforms:
        scraper = PLATFORM_SCRAPERS[platform]
        tasks.append(scraper.scrape_products(q))
    
    results = await asyncio.gather(*tasks)
    products = [product for platform_results in results for product in platform_results]
    
    return products

@app.get("/lowest", response_model=Product)
async def get_lowest_price(q: str):
    products = await search_products(q)
    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    return min(products, key=lambda x: x["price"])

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)