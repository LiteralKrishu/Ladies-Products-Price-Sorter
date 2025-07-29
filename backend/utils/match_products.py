from fuzzywuzzy import fuzz
import re
from typing import List, Dict
from ..models.product import Product

def normalize_title(title: str) -> str:
    """Clean and standardize product titles for comparison"""
    # Remove common non-essential parts
    removals = [
        r'\b\d+ml\b', r'\b\d+g\b', r'\b\d+oz\b',  # Quantities
        r'\b(?:pack of|set of) \d+\b',            # Pack sizes
        r'\b(?:free\s)?shipping\b',               # Shipping info
        r'\b\d+% off\b',                          # Discount mentions
        r'\[[^\]]*\]', '\([^\)]*\)',             # Bracketed content
        r'\b(?:with|without|for|and|the|a|an)\b'  # Common words
    ]
    
    for pattern in removals:
        title = re.sub(pattern, '', title, flags=re.IGNORECASE)
    
    # Standardize variations
    replacements = {
        r'\beye\b': 'eyeshadow',
        r'\blip\b': 'lipstick',
        r'\bmatte\b': 'matte',
        r'\bwaterproof\b': 'waterproof'
    }
    
    for pattern, replacement in replacements.items():
        title = re.sub(pattern, replacement, title, flags=re.IGNORECASE)
    
    return title.strip().lower()

def calculate_similarity(product1: Dict, product2: Dict) -> float:
    """Calculate similarity score between two products (0-100)"""
    title1 = normalize_title(product1['title'])
    title2 = normalize_title(product2['title'])
    
    # Weighted combination of different matching strategies
    token_set_ratio = fuzz.token_set_ratio(title1, title2)
    token_sort_ratio = fuzz.token_sort_ratio(title1, title2)
    partial_ratio = fuzz.partial_ratio(title1, title2)
    
    # Average with slight preference for token set
    similarity = (token_set_ratio * 0.5 + token_sort_ratio * 0.3 + partial_ratio * 0.2)
    
    # Penalize for brand mismatch
    brand_words = ['maybelline', 'lakme', 'loreal', 'huda', 'nykaa', 'mac']
    brand1 = any(brand in title1 for brand in brand_words)
    brand2 = any(brand in title2 for brand in brand_words)
    
    if brand1 and brand2 and not any(brand in title1 and brand in title2 for brand in brand_words):
        similarity *= 0.7  # 30% penalty for brand mismatch
    
    return similarity

def group_similar_products(products: List[Dict], threshold: float = 85.0) -> List[List[Dict]]:
    """Group similar products across different platforms"""
    if not products:
        return []
    
    groups = []
    remaining_products = products.copy()
    
    while remaining_products:
        current = remaining_products.pop()
        group = [current]
        
        to_remove = []
        for i, product in enumerate(remaining_products):
            similarity = calculate_similarity(current, product)
            if similarity >= threshold:
                group.append(product)
                to_remove.append(i)
        
        # Remove matched products in reverse order
        for i in sorted(to_remove, reverse=True):
            remaining_products.pop(i)
        
        groups.append(group)
    
    return groups