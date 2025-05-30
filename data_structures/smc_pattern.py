from dataclasses import dataclass
from datetime import datetime


@dataclass
class SMCPattern:
    """Smart Money Concepts pattern"""
    pattern_type: str  # 'ORDER_BLOCK', 'FVG', 'LIQUIDITY_SWEEP', 'BOS', 'CHOCH'
    direction: str  # 'BULLISH', 'BEARISH'
    confidence: float  # 0-100
    price_level: float
    timestamp: datetime
    zone_high: float
    zone_low: float
    description: str