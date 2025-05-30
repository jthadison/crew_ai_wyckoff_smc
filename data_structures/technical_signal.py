from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict


@dataclass
class TechnicalSignal:
    """Technical analysis signal"""
    signal_type: str
    strength: float  # 0-10 scale
    price_level: float
    timestamp: datetime
    timeframe: str
    description: str
    confidence: float  # 0-1 scale
    parameters: Dict[str, Any]