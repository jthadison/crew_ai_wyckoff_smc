"""
Data structures package for the Wyckoff/SMC trading system
"""

try:
    from .ohlc import OHLCData
    from .trade_results import TradeResult
    from .confluence_signal import ConfluenceSignal
    from .wyckoff_pattern import WyckoffPattern
    from .smc_pattern import SMCPattern
    from .performance_metrics import PerformanceMetrics
    from .pattern_results import PatternResult
    from .pattern_performance import PatternPerformance
    
    __all__ = [
        'OHLCData',
        'TradeResult', 
        'ConfluenceSignal',
        'WyckoffPattern',
        'SMCPattern',
        'PerformanceMetrics',
        'PatternResult',
        'PatternPerformance'
    ]
except ImportError as e:
    # Some modules might not exist yet
    print(f"Warning: Could not import all data structures: {e}")
    __all__ = []
