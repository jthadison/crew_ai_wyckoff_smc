from dataclasses import dataclass
from datetime import datetime
from typing import List, Tuple


@dataclass
class OrderBlock:
    """Smart Money Order Block"""
    block_type: str  # 'bullish', 'bearish'
    price_range: Tuple[float, float]  # (low, high)
    formation_time: datetime
    retest_times: List[datetime]
    strength: float  # Based on volume and price action
    status: str  # 'active', 'mitigated', 'breached'
    timeframe: str