from dataclasses import dataclass


@dataclass
class PatternPerformance:
    """Pattern-specific performance tracking"""
    pattern_name: str
    pattern_type: str
    total_occurrences: int
    winning_occurrences: int
    success_rate: float
    avg_pnl: float
    avg_confidence_when_detected: float
    avg_confidence_when_successful: float
    avg_hold_time_hours: float
    reliability_score: float