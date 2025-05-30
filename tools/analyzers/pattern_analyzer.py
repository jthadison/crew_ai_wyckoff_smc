from collections import defaultdict
import statistics
from typing import List

from data_structures.pattern_performance import PatternPerformance
from data_structures.trade_results import TradeResult


class PatternAnalyzer:
    """Analyze pattern performance and effectiveness"""
    
    @staticmethod
    def analyze_pattern_performance(trades: List[TradeResult]) -> List[PatternPerformance]:
        """Analyze performance of different patterns"""
        pattern_stats = defaultdict(lambda: {
            'total': 0,  # Ensure this is always an int
            'wins': 0,
            'total_pnl': 0.0,  # Use float for PnL
            'confidence_scores': [],
            'winning_confidence_scores': [],
            'hold_times': []
        })
        
        for trade in trades:
            for pattern in trade.patterns_detected:
                stats = pattern_stats[pattern]
                if not isinstance(stats['total'], int):
                    stats['total'] = 0
                stats['total'] += 1
                if trade.pnl is not None:
                    if not isinstance(stats['total_pnl'], (int, float)):
                        stats['total_pnl'] = 0.0
                    stats['total_pnl'] += float(trade.pnl)
                if not isinstance(stats['confidence_scores'], list):
                    stats['confidence_scores'] = []
                stats['confidence_scores'].append(trade.confluence_score)
                
                if trade.hold_time_hours:
                    if not isinstance(stats['hold_times'], list):
                        stats['hold_times'] = []
                    stats['hold_times'].append(trade.hold_time_hours)
                
                if trade.pnl is not None and trade.pnl > 0:
                    if not isinstance(stats['wins'], int):
                        stats['wins'] = 0
                    stats['wins'] += 1
                    if not isinstance(stats['winning_confidence_scores'], list):
                        stats['winning_confidence_scores'] = []
                    stats['winning_confidence_scores'].append(trade.confluence_score)
        
        pattern_performances = []
        for pattern_name, stats in pattern_stats.items():
            if isinstance(stats['total'], (int, float)) and not isinstance(stats['total'], list) and stats['total'] > 0 and isinstance(stats['wins'], (int, float)) and not isinstance(stats['wins'], list):
                success_rate = (stats['wins'] / stats['total']) * 100
                avg_pnl = (stats['total_pnl'] / stats['total']
                           if isinstance(stats['total_pnl'], (int, float)) and not isinstance(stats['total_pnl'], list) and stats['total'] != 0
                           else 0)
                confidence_scores = stats['confidence_scores'] if isinstance(stats['confidence_scores'], list) else []
                avg_confidence = statistics.mean(confidence_scores) if confidence_scores else 0
                winning_conf_scores = stats['winning_confidence_scores'] if isinstance(stats['winning_confidence_scores'], list) else []
                avg_winning_confidence = statistics.mean(winning_conf_scores) if winning_conf_scores else 0
                avg_hold_time = (statistics.mean(stats['hold_times']) 
                               if isinstance(stats['hold_times'], list) and stats['hold_times'] else 0)
                
                # Calculate reliability score (weighted by success rate and frequency)
                total_occurrences = stats['total'] if isinstance(stats['total'], (int, float)) else 0
                frequency_weight = min(1.0, total_occurrences / 10)  # More weight for frequently seen patterns
                reliability_score = (success_rate * 0.7 + avg_confidence * 0.3) * frequency_weight
                
                pattern_performances.append(PatternPerformance(
                    pattern_name=pattern_name,
                    pattern_type="UNKNOWN",  # Could be enhanced to detect type
                    total_occurrences=int(stats['total']) if not isinstance(stats['total'], list) else 0,
                    winning_occurrences=int(stats['wins']) if not isinstance(stats['wins'], list) else 0,
                    success_rate=success_rate,
                    avg_pnl=avg_pnl,
                    avg_confidence_when_detected=avg_confidence,
                    avg_confidence_when_successful=avg_winning_confidence,
                    avg_hold_time_hours=avg_hold_time,
                    reliability_score=reliability_score
                ))
        
        return sorted(pattern_performances, key=lambda x: x.reliability_score, reverse=True)