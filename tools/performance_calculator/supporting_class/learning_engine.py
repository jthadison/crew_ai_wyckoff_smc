from typing import List, Dict, Any
from datetime import datetime
import statistics

# Define PatternPerformance as a placeholder or import it from the correct module
class PatternPerformance:
    def __init__(self, pattern_name: str, reliability_score: float):
        self.pattern_name = pattern_name
        self.reliability_score = reliability_score

# Define TradeResult as a placeholder or import it from the correct module
class TradeResult:
    def __init__(self, confluence_score: float, pnl: float, wyckoff_signals=None, smc_signals=None, patterns_detected=None):
        self.confluence_score = confluence_score
        self.pnl = pnl
        self.wyckoff_signals = wyckoff_signals
        self.smc_signals = smc_signals
        self.patterns_detected = patterns_detected

class LearningEngine:
    """Machine learning component for system optimization"""
    
    def __init__(self):
        self.confluence_weights = {
            'wyckoff_weight': 0.40,
            'smc_weight': 0.30,
            'technical_weight': 0.20,
            'pattern_weight': 0.10
        }
        self.pattern_reliability_scores = {}
        self.optimization_history = []
    
    def analyze_confluence_effectiveness(self, trades: List[TradeResult]) -> Dict[str, float]:
        """Analyze which confluence factors are most effective"""
        if len(trades) < 10:  # Need minimum trades for analysis
            return self.confluence_weights
        
        # Separate trades by confluence score ranges
        high_conf_trades = [t for t in trades if t.confluence_score >= 80]
        med_conf_trades = [t for t in trades if 70 <= t.confluence_score < 80]
        low_conf_trades = [t for t in trades if t.confluence_score < 70]
        
        # Calculate success rates for each group
        high_conf_success = self._calculate_success_rate(high_conf_trades)
        med_conf_success = self._calculate_success_rate(med_conf_trades)
        low_conf_success = self._calculate_success_rate(low_conf_trades)
        
        # Analyze signal type effectiveness
        wyckoff_effectiveness = self._analyze_signal_effectiveness(trades, 'wyckoff_signals')
        smc_effectiveness = self._analyze_signal_effectiveness(trades, 'smc_signals')
        pattern_effectiveness = self._analyze_pattern_effectiveness(trades)
        
        # Calculate new weights based on effectiveness
        total_effectiveness = (wyckoff_effectiveness + smc_effectiveness + 
                              pattern_effectiveness + 50)  # 50 for technical baseline
        
        new_weights = {
            'wyckoff_weight': wyckoff_effectiveness / total_effectiveness,
            'smc_weight': smc_effectiveness / total_effectiveness,
            'pattern_weight': pattern_effectiveness / total_effectiveness,
            'technical_weight': 50 / total_effectiveness  # Baseline technical weight
        }
        
        # Normalize weights to sum to 1.0
        weight_sum = sum(new_weights.values())
        for key in new_weights:
            new_weights[key] /= weight_sum
        
        # Record optimization
        self.optimization_history.append({
            'timestamp': datetime.now(),
            'old_weights': self.confluence_weights.copy(),
            'new_weights': new_weights.copy(),
            'high_conf_success': high_conf_success,
            'med_conf_success': med_conf_success,
            'low_conf_success': low_conf_success,
            'total_trades_analyzed': len(trades)
        })
        
        self.confluence_weights = new_weights
        return new_weights
    
    def _calculate_success_rate(self, trades: List[TradeResult]) -> float:
        """Calculate success rate for a group of trades"""
        if not trades:
            return 0
        
        successful_trades = len([t for t in trades if t.pnl and t.pnl > 0])
        return (successful_trades / len(trades)) * 100
    
    def _analyze_signal_effectiveness(self, trades: List[TradeResult], signal_field: str) -> float:
        """Analyze effectiveness of specific signal types"""
        signal_trades = [t for t in trades if getattr(t, signal_field)]
        if not signal_trades:
            return 50  # Baseline score
        
        success_rate = self._calculate_success_rate(signal_trades)
        return success_rate
    
    def _analyze_pattern_effectiveness(self, trades: List[TradeResult]) -> float:
        """Analyze effectiveness of pattern-based trades"""
        pattern_trades = [t for t in trades if t.patterns_detected]
        if not pattern_trades:
            return 50  # Baseline score
        
        success_rate = self._calculate_success_rate(pattern_trades)
        return success_rate
    
    def update_pattern_reliability(self, pattern_performances: List[PatternPerformance]):
        """Update pattern reliability scores based on performance"""
        for pattern_perf in pattern_performances:
            self.pattern_reliability_scores[pattern_perf.pattern_name] = pattern_perf.reliability_score
    
    def generate_optimization_insights(self) -> Dict[str, Any]:
        """Generate insights from optimization history"""
        if not self.optimization_history:
            return {"message": "No optimization history available"}
        
        latest = self.optimization_history[-1]
        
        insights = {
            'latest_optimization': latest,
            'weight_changes': {},
            'performance_trend': {},
            'recommendations': []
        }
        
        # Calculate weight changes
        for key in latest['new_weights']:
            old_val = latest['old_weights'][key]
            new_val = latest['new_weights'][key]
            change = ((new_val - old_val) / old_val) * 100 if old_val > 0 else 0
            insights['weight_changes'][key] = {
                'old': old_val,
                'new': new_val,
                'change_percent': change
            }
        
        # Generate recommendations
        if latest['high_conf_success'] > 75:
            insights['recommendations'].append("High confidence signals performing well - consider increasing minimum confluence threshold")
        
        if latest['high_conf_success'] < 60:
            insights['recommendations'].append("High confidence signals underperforming - review confluence calculation")
        
        # Analyze weight stability
        if len(self.optimization_history) > 3:
            recent_optimizations = self.optimization_history[-3:]
            wyckoff_weights = [opt['new_weights']['wyckoff_weight'] for opt in recent_optimizations]
            wyckoff_stability = statistics.stdev(wyckoff_weights)
            
            if wyckoff_stability < 0.05:
                insights['recommendations'].append("Wyckoff weights stabilizing - good convergence")
            else:
                insights['recommendations'].append("Wyckoff weights still adjusting - continue monitoring")
        
        return insights