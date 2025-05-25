import random
from core.config import PROXY_POOL

# Proxy statistics are maintained at module level
_proxy_stats = {proxy: {"success": 0, "failures": 0} for proxy in PROXY_POOL}

def get_weighted_proxy():
    """
    Select a proxy based on its success-to-failure weight.
    """
    weights = [
        (stats["success"] + 1) / (stats["failures"] + 1)  # Avoid division by zero
        for stats in _proxy_stats.values()
    ]
    return random.choices(list(_proxy_stats.keys()), weights=weights, k=1)[0]

def report_proxy_result(proxy: str, success: bool):
    """
    Update success/failure count of the given proxy.
    """
    if proxy in _proxy_stats:
        if success:
            _proxy_stats[proxy]["success"] += 1
        else:
            _proxy_stats[proxy]["failures"] += 1

def get_proxy_stats():
    """
    Optional: expose proxy stats for debugging/logging.
    """
    return _proxy_stats.copy()
