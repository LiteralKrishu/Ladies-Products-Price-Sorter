from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    title: str
    price: float
    original_price: Optional[float] = None
    discount: Optional[str] = None
    rating: Optional[float] = None
    platform: str
    image_url: Optional[str] = None
    product_link: str
    in_stock: bool = True
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Maybelline Fit Me Foundation - 120 Classic Ivory",
                "price": 449.0,
                "original_price": 499.0,
                "discount": "10%",
                "rating": 4.4,
                "platform": "Amazon",
                "image_url": "https://example.com/image.jpg",
                "product_link": "https://amazon.in/product/123",
                "in_stock": True
            }
        }