from dataclasses import dataclass
from datetime import timedelta
from typing import Dict, Optional


@dataclass
class PatternResult:
    """Pattern recognition result"""
    pattern_name: str
    pattern_type: str  # 'CHART', 'CANDLESTICK', 'WYCKOFF', 'SMC', 'HARMONIC'
    direction: str  # 'BULLISH', 'BEARISH', 'NEUTRAL', 'REVERSAL', 'CONTINUATION'
    confidence: float  # 0-100
    start_index: int
    end_index: int
    key_levels: Dict[str, float]
    target_price: Optional[float]
    stop_loss: Optional[float]
    formation_time: timedelta
    description: str
    reliability_score: float  # Historical success rate