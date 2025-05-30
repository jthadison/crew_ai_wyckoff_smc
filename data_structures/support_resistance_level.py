from dataclasses import dataclass
from datetime import datetime


@dataclass
class SupportResistanceLevel:
    """Support/Resistance level"""
    price: float
    strength: int  # Number of touches/tests
    level_type: str  # 'support' or 'resistance'
    first_touch: datetime
    last_touch: datetime
    timeframe: str