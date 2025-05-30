from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Tuple


@dataclass
class FairValueGap:
    """Fair Value Gap (Imbalance)"""
    gap_type: str  # 'bullish', 'bearish'
    gap_range: Tuple[float, float]  # (low, high)
    formation_time: datetime
    fill_percentage: float  # How much of the gap has been filled
    volume_profile: Dict[str, float]
    priority: str  # 'high', 'medium', 'low'