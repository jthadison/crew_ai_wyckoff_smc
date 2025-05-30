from datetime import datetime
import json
from typing import Dict, List
from crewai.tools import BaseTool

from data_structures.performance_metrics import PerformanceMetrics
from data_structures.trade_results import TradeResult
from tools.analyzers.pattern_analyzer import PatternAnalyzer
from tools.performance_calculator.supporting_class.learning_engine import LearningEngine
from tools.performance_calculator.supporting_class.performance_calculator import PerformanceCalculator

class PerformanceAnalyticsTool(BaseTool):
    """Main Performance Analytics Tool for CrewAI integration"""
    
    name: str = "performance_analytics"
    description: str = "Comprehensive performance tracking, analysis, and system optimization"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        object.__setattr__(self, '_trades_database', [])
        object.__setattr__(self, '_calculator', PerformanceCalculator())
        object.__setattr__(self, '_pattern_analyzer', PatternAnalyzer())
        object.__setattr__(self, '_learning_engine', LearningEngine())
        object.__setattr__(self, '_last_recalibration', datetime.now())
        object.__setattr__(self, '_recalibration_frequency', 5)  # Every 5 trades
    
    @property
    def trades_database(self) -> List[TradeResult]:
        return object.__getattribute__(self, '_trades_database') if hasattr(self, '_trades_database') else []
    
    @property
    def calculator(self) -> PerformanceCalculator:
        return object.__getattribute__(self, '_calculator') if hasattr(self, '_calculator') else PerformanceCalculator()
    
    @property
    def pattern_analyzer(self) -> PatternAnalyzer:
        return object.__getattribute__(self, '_pattern_analyzer') if hasattr(self, '_pattern_analyzer') else PatternAnalyzer()
    
    @property
    def learning_engine(self) -> LearningEngine:
        return object.__getattribute__(self, '_learning_engine') if hasattr(self, '_learning_engine') else LearningEngine()
    
    def _run(self, action: str, data: str = "") -> str:
        """
        Run performance analytics
        
        Args:
            action: 'analyze', 'add_trade', 'optimize', 'report', 'patterns'
            data: JSON string with relevant data
        """
        try:
            if action == "analyze":
                return self._analyze_performance()
            
            elif action == "add_trade":
                trade_data = json.loads(data) if data else {}
                return self._add_trade_result(trade_data)
            
            elif action == "optimize":
                return self._optimize_system()
            
            elif action == "report":
                report_type = json.loads(data).get('type', 'comprehensive') if data else 'comprehensive'
                return self._generate_report(report_type)
            
            elif action == "patterns":
                return self._analyze_patterns()
            
            else:
                return f"Unknown action: {action}. Available actions: analyze, add_trade, optimize, report, patterns"
        
        except Exception as e:
            return f"Error in performance analytics: {str(e)}"
    
    def _analyze_performance(self) -> str:
        """Analyze current performance metrics"""
        if not self.trades_database:
            return "No trade data available for analysis"
        
        metrics = self.calculator.calculate_basic_metrics(self.trades_database)
        
        output = []
        output.append("📊 PERFORMANCE ANALYSIS")
        output.append("=" * 50)
        output.append(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output.append(f"Total Trades: {metrics.total_trades}")
        output.append("")
        
        # Basic metrics
        output.append("📈 BASIC METRICS")
        output.append("-" * 25)
        output.append(f"Win Rate: {metrics.win_rate:.1f}%")
        output.append(f"Profit Factor: {metrics.profit_factor:.2f}")
        output.append(f"Total P&L: ${metrics.total_pnl:.2f}")
        output.append(f"Total P&L %: {metrics.total_pnl_percent:.2f}%")
        output.append(f"Average Win: ${metrics.avg_win:.2f}")
        output.append(f"Average Loss: ${metrics.avg_loss:.2f}")
        output.append(f"Expectancy: ${metrics.expectancy:.2f}")
        output.append("")
        
        # Risk metrics
        output.append("⚠️ RISK METRICS")
        output.append("-" * 25)
        output.append(f"Max Drawdown: ${metrics.max_drawdown:.2f} ({metrics.max_drawdown_percent:.1f}%)")
        output.append(f"Max Consecutive Losses: {metrics.max_consecutive_losses}")
        output.append(f"Sharpe Ratio: {metrics.sharpe_ratio:.2f}")
        output.append(f"Sortino Ratio: {metrics.sortino_ratio:.2f}")
        output.append(f"Recovery Factor: {metrics.recovery_factor:.2f}")
        output.append("")
        
        # Asset performance
        if metrics.profit_factor_by_asset:
            output.append("💱 ASSET PERFORMANCE")
            output.append("-" * 25)
            for asset, pf in sorted(metrics.profit_factor_by_asset.items(), 
                                  key=lambda x: x[1], reverse=True):
                output.append(f"{asset}: {pf:.2f}")
            output.append("")
        
        # Performance rating
        rating = self._calculate_performance_rating(metrics)
        output.append(f"🎯 OVERALL RATING: {rating}")
        
        return "\n".join(output)
    
    def _add_trade_result(self, trade_data: Dict) -> str:
        """Add a new trade result to the database"""
        try:
            trade = TradeResult(
                trade_id=trade_data.get('trade_id', f"trade_{len(self.trades_database) + 1}"),
                symbol=trade_data.get('symbol', 'UNKNOWN'),
                timeframe=trade_data.get('timeframe', '1H'),
                entry_time=datetime.fromisoformat(trade_data.get('entry_time', datetime.now().isoformat())),
                exit_time=datetime.fromisoformat(trade_data['exit_time']) if trade_data.get('exit_time') else None,
                entry_price=trade_data.get('entry_price', 0.0),
                exit_price=trade_data.get('exit_price'),
                position_size=trade_data.get('position_size', 0.0),
                trade_type=trade_data.get('trade_type', 'BUY'),
                status=trade_data.get('status', 'OPEN'),
                pnl=trade_data.get('pnl'),
                pnl_percent=trade_data.get('pnl_percent'),
                stop_loss=trade_data.get('stop_loss', 0.0),
                take_profit=trade_data.get('take_profit', 0.0),
                patterns_detected=trade_data.get('patterns_detected', []),
                confluence_score=trade_data.get('confluence_score', 0.0),
                wyckoff_signals=trade_data.get('wyckoff_signals', []),
                smc_signals=trade_data.get('smc_signals', []),
                technical_indicators=trade_data.get('technical_indicators', {}),
                risk_reward_ratio=trade_data.get('risk_reward_ratio', 0.0),
                hold_time_hours=trade_data.get('hold_time_hours'),
                max_favorable_excursion=trade_data.get('max_favorable_excursion'),
                max_adverse_excursion=trade_data.get('max_adverse_excursion'),
                trade_notes=trade_data.get('trade_notes', '')
            )
            
            # Add to database
            current_trades = list(self.trades_database)
            current_trades.append(trade)
            object.__setattr__(self, '_trades_database', current_trades)
            
            # Check if recalibration is needed
            closed_trades = [t for t in current_trades if t.status == 'CLOSED']
            if len(closed_trades) % self._recalibration_frequency == 0:
                self._trigger_recalibration()
            
            return f"✅ Trade {trade.trade_id} added successfully. Total trades: {len(current_trades)}"
        
        except Exception as e:
            return f"❌ Error adding trade: {str(e)}"
    
    def _optimize_system(self) -> str:
        """Optimize system parameters based on performance"""
        closed_trades = [t for t in self.trades_database if t.status == 'CLOSED']
        
        if len(closed_trades) < 10:
            return "❌ Insufficient trade data for optimization (minimum 10 closed trades required)"
        
        # Optimize confluence weights
        new_weights = self.learning_engine.analyze_confluence_effectiveness(closed_trades)
        
        # Analyze pattern performance
        pattern_performances = self.pattern_analyzer.analyze_pattern_performance(closed_trades)
        self.learning_engine.update_pattern_reliability(pattern_performances)
        
        # Generate insights
        insights = self.learning_engine.generate_optimization_insights()
        
        output = []
        output.append("🧠 SYSTEM OPTIMIZATION")
        output.append("=" * 50)
        output.append(f"Optimization Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output.append(f"Trades Analyzed: {len(closed_trades)}")
        output.append("")
        
        # New weights
        output.append("⚖️ UPDATED CONFLUENCE WEIGHTS")
        output.append("-" * 35)
        for weight_name, weight_value in new_weights.items():
            old_value = insights['weight_changes'][weight_name]['old']
            change = insights['weight_changes'][weight_name]['change_percent']
            arrow = "📈" if change > 0 else "📉" if change < 0 else "➡️"
            output.append(f"{weight_name}: {weight_value:.3f} {arrow} ({change:+.1f}%)")
        output.append("")
        
        # Top performing patterns
        if pattern_performances:
            output.append("🎯 TOP PERFORMING PATTERNS")
            output.append("-" * 35)
            for pattern in pattern_performances[:5]:
                output.append(f"{pattern.pattern_name}: {pattern.success_rate:.1f}% success rate")
        output.append("")
        
        # Recommendations
        if insights['recommendations']:
            output.append("💡 OPTIMIZATION RECOMMENDATIONS")
            output.append("-" * 35)
            for rec in insights['recommendations']:
                output.append(f"• {rec}")
        
        # Update last recalibration time
        object.__setattr__(self, '_last_recalibration', datetime.now())
        
        return "\n".join(output)
    
    def _analyze_patterns(self) -> str:
        """Analyze pattern performance in detail"""
        closed_trades = [t for t in self.trades_database if t.status == 'CLOSED']
        
        if not closed_trades:
            return "No closed trades available for pattern analysis"
        
        pattern_performances = self.pattern_analyzer.analyze_pattern_performance(closed_trades)
        
        output = []
        output.append("🎨 PATTERN PERFORMANCE ANALYSIS")
        output.append("=" * 50)
        output.append(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output.append(f"Patterns Analyzed: {len(pattern_performances)}")
        output.append("")
        
        for pattern in pattern_performances:
            output.append(f"📊 {pattern.pattern_name}")
            output.append(f"   Success Rate: {pattern.success_rate:.1f}%")
            output.append(f"   Total Occurrences: {pattern.total_occurrences}")
            output.append(f"   Avg P&L: ${pattern.avg_pnl:.2f}")
            output.append(f"   Avg Confidence: {pattern.avg_confidence_when_detected:.1f}%")
            output.append(f"   Reliability Score: {pattern.reliability_score:.1f}")
            output.append("")
        
        return "\n".join(output)
    
    def _generate_report(self, report_type: str) -> str:
        """Generate comprehensive performance report"""
        if report_type == "comprehensive":
            return self._generate_comprehensive_report()
        elif report_type == "summary":
            return self._generate_summary_report()
        elif report_type == "optimization":
            return self._optimize_system()
        else:
            return f"Unknown report type: {report_type}"
    
    def _generate_comprehensive_report(self) -> str:
        """Generate detailed comprehensive report"""
        performance_analysis = self._analyze_performance()
        pattern_analysis = self._analyze_patterns()
        optimization_status = self._get_optimization_status()
        
        return f"{performance_analysis}\n\n{pattern_analysis}\n\n{optimization_status}"
    
    def _generate_summary_report(self) -> str:
        """Generate summary report"""
        if not self.trades_database:
            return "No trade data available for summary"
        
        metrics = self.calculator.calculate_basic_metrics(self.trades_database)
        rating = self._calculate_performance_rating(metrics)
        
        return f"""
📊 PERFORMANCE SUMMARY
=====================
Total Trades: {metrics.total_trades}
Win Rate: {metrics.win_rate:.1f}%
Profit Factor: {metrics.profit_factor:.2f}
Total P&L: ${metrics.total_pnl:.2f}
Max Drawdown: {metrics.max_drawdown_percent:.1f}%
Overall Rating: {rating}
        """.strip()
    
    def _get_optimization_status(self) -> str:
        """Get current optimization status"""
        time_since_last = datetime.now() - self._last_recalibration
        closed_trades = len([t for t in self.trades_database if t.status == 'CLOSED'])
        
        output = []
        output.append("🔧 OPTIMIZATION STATUS")
        output.append("=" * 50)
        output.append(f"Last Recalibration: {self._last_recalibration.strftime('%Y-%m-%d %H:%M:%S')}")
        output.append(f"Time Since Last: {time_since_last}")
        output.append(f"Closed Trades: {closed_trades}")
        output.append(f"Next Recalibration: Every {self._recalibration_frequency} trades")
        
        trades_until_next = self._recalibration_frequency - (closed_trades % self._recalibration_frequency)
        output.append(f"Trades Until Next: {trades_until_next}")
        
        return "\n".join(output)
    
    def _trigger_recalibration(self):
        """Trigger system recalibration"""
        self._optimize_system()
    
    def _calculate_performance_rating(self, metrics: PerformanceMetrics) -> str:
        """Calculate overall performance rating"""
        score = 0
        
        # Win rate scoring (0-25 points)
        if metrics.win_rate >= 70:
            score += 25
        elif metrics.win_rate >= 60:
            score += 20
        elif metrics.win_rate >= 50:
            score += 15
        elif metrics.win_rate >= 40:
            score += 10
        
        # Profit factor scoring (0-25 points)
        if metrics.profit_factor >= 2.0:
            score += 25
        elif metrics.profit_factor >= 1.5:
            score += 20
        elif metrics.profit_factor >= 1.2:
            score += 15
        elif metrics.profit_factor >= 1.0:
            score += 10
        
        # Drawdown scoring (0-25 points)
        if metrics.max_drawdown_percent <= 5:
            score += 25
        elif metrics.max_drawdown_percent <= 10:
            score += 20
        elif metrics.max_drawdown_percent <= 15:
            score += 15
        elif metrics.max_drawdown_percent <= 25:
            score += 10
        
        # Sharpe ratio scoring (0-25 points)
        if metrics.sharpe_ratio >= 2.0:
            score += 25
        elif metrics.sharpe_ratio >= 1.5:
            score += 20
        elif metrics.sharpe_ratio >= 1.0:
            score += 15
        elif metrics.sharpe_ratio >= 0.5:
            score += 10
        
        # Convert to rating
        if score >= 80:
            return "🏆 EXCELLENT"
        elif score >= 60:
            return "👍 GOOD"
        elif score >= 40:
            return "📊 AVERAGE"
        elif score >= 20:
            return "⚠️ POOR"
        else:
            return "❌ VERY POOR"