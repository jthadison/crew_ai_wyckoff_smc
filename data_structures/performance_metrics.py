from dataclasses import dataclass
from typing import Dict

@dataclass
class PerformanceMetrics:
    """Comprehensive performance metrics"""
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    profit_factor: float
    total_pnl: float
    total_pnl_percent: float
    avg_win: float
    avg_loss: float
    largest_win: float
    largest_loss: float
    max_consecutive_wins: int
    max_consecutive_losses: int
    max_drawdown: float
    max_drawdown_percent: float
    sharpe_ratio: float
    sortino_ratio: float
    calmar_ratio: float
    avg_trade_duration_hours: float
    avg_risk_reward: float
    expectancy: float
    recovery_factor: float
    profit_factor_by_asset: Dict[str, float]
    performance_by_timeframe: Dict[str, Dict]