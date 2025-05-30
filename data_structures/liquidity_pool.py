from dataclasses import dataclass
from datetime import datetime
from typing import Tuple


@dataclass
class LiquidityPool:
    """Liquidity accumulation zone"""
    pool_type: str  # 'buy_side', 'sell_side'
    price_level: float
    accumulation_period: Tuple[datetime, datetime]
    estimated_volume: float
    sweep_probability: float  # 0-1 scale
    protection_level: float  # Stop loss cluster level