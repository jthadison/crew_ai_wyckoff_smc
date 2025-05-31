from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List

from data_structures.performance_metrics import PerformanceMetrics
from data_structures.trade_results import TradeResult


@dataclass
class BacktestResult:
    """Backtest execution result"""
    strategy_name: str
    parameters: Dict[str, Any]
    start_date: datetime
    end_date: datetime
    total_trades: int
    performance_metrics: PerformanceMetrics
    trades: List[TradeResult]
    confidence_score: float
    parameter_stability: float
    market_regime_performance: Dict[str, Dict]
    statistical_significance: float
    recommendation: str
    detailed_analysis: str