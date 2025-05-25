import re

def normalize_price(price_str: str) -> int:
    if not price_str:
        return 10**9
    cleaned = re.sub(r'[^\d]', '', price_str)
    try:
        return int(cleaned)
    except ValueError:
        return 10**9

def normalize_discount(discount_str: str) -> int:
    if not discount_str:
        return 0
    match = re.search(r'(\d+)', discount_str)
    return int(match.group(1)) if match else 0

def normalize_rating(rating_str: str) -> float:
    try:
        return float(rating_str.split()[0])
    except Exception:
        return 0.0

def normalize_delivery_time(delivery_str: str) -> int:
    if not delivery_str:
        return 999
    if "next day" in delivery_str.lower():
        return 1
    nums = re.findall(r'\d+', delivery_str)
    if not nums:
        return 999
    nums = list(map(int, nums))
    return sum(nums) // len(nums)
