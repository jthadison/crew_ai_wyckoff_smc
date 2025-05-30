from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class TradeResult:
    """Individual trade result data"""
    trade_id: str
    symbol: str
    timeframe: str
    entry_time: datetime
    exit_time: Optional[datetime]
    entry_price: float
    exit_price: Optional[float]
    position_size: float
    trade_type: str  # 'BUY', 'SELL'
    status: str  # 'OPEN', 'CLOSED', 'STOPPED'
    pnl: Optional[float]
    pnl_percent: Optional[float]
    stop_loss: float
    take_profit: float
    patterns_detected: List[str]
    confluence_score: float
    wyckoff_signals: List[str]
    smc_signals: List[str]
    technical_indicators: Dict[str, float]
    risk_reward_ratio: float
    hold_time_hours: Optional[float]
    max_favorable_excursion: Optional[float]  # MFE
    max_adverse_excursion: Optional[float]    # MAE
    trade_notes: str