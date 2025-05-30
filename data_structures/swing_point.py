from dataclasses import dataclass
from datetime import datetime


@dataclass
class SwingPoint:
    """Swing high/low point"""
    price: float
    timestamp: datetime
    point_type: str  # 'high' or 'low'
    index: int
    strength: int  # How many bars on each side
    timeframe: str