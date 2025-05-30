from datetime import datetime, timedelta
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class MarketStructure:
    """Market structure analysis data"""
    symbol: str
    bias: str  # 'bullish', 'bearish', 'neutral'
    swing_highs: List[Dict[str, Any]]
    swing_lows: List[Dict[str, Any]]
    support_levels: List[float]
    resistance_levels: List[float]
    trend_change: bool
    institutional_levels: List[float]