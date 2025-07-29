from typing import List, Optional
from pydantic import BaseModel
from .product import Product

class APIResponse(BaseModel):
    success: bool
    message: Optional[str] = None

class SearchResponse(APIResponse):
    query: str
    count: int
    results: List[Product]
    groups: Optional[List[List[Product]]] = None

class LowestPriceResponse(APIResponse):
    query: str
    product: Optional[Product] = None
    alternatives: Optional[List[Product]] = None

class ErrorResponse(APIResponse):
    error_type: str
    details: Optional[str] = None