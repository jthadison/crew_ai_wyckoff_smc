from dataclasses import dataclass
from datetime import datetime


@dataclass
class MarketRegime:
    """Market regime classification"""
    regime_type: str  # 'TRENDING_UP', 'TRENDING_DOWN', 'SIDEWAYS', 'HIGH_VOLATILITY'
    start_date: datetime
    end_date: datetime
    volatility: float
    trend_strength: float