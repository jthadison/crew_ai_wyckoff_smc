from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class ConfluenceSignal:
    """Combined Wyckoff + SMC signal with confluence scoring"""
    signal_type: str  # 'BUY', 'SELL'
    confluence_score: float  # 0-100
    entry_price: float
    stop_loss: float
    take_profit: float
    risk_reward_ratio: float
    wyckoff_patterns: List[str]
    smc_patterns: List[str]
    supporting_indicators: List[str]
    timestamp: datetime
    reasoning: str