from datetime import datetime
import json
import statistics
from typing import Dict, List
from crewai.tools import BaseTool

from data_structures.performance_metrics import PerformanceMetrics
from tools.performance_calculator.supporting_class.learning_engine import TradeResult as LearningEngineTradeResult, LearningEngine
from data_structures.trade_results import TradeResult
from tools.analyzers.pattern_analyzer import PatternAnalyzer
from tools.performance_calculator.supporting_class.performance_calculator import PerformanceCalculator

class PerformanceAnalyticsTool(BaseTool):
    """Enhanced Performance Analytics Tool with advanced monitoring and ML capabilities"""
    
    name: str = "enhanced_performance_analytics"
    description: str = "Advanced performance tracking, real-time monitoring, and AI-powered trade analysis with predictive capabilities"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Core components
        object.__setattr__(self, '_trades_database', [])
        object.__setattr__(self, '_calculator', PerformanceCalculator())
        object.__setattr__(self, '_pattern_analyzer', PatternAnalyzer())
        object.__setattr__(self, '_learning_engine', LearningEngine())
        object.__setattr__(self, '_last_recalibration', datetime.now())
        object.__setattr__(self, '_recalibration_frequency', 5)  # Every 5 trades
        
        # Enhanced features
        object.__setattr__(self, '_performance_history', [])
        object.__setattr__(self, '_alerts_config', self._default_alerts_config())
        object.__setattr__(self, '_real_time_metrics', {})
        object.__setattr__(self, '_predictions', {})
        object.__setattr__(self, '_last_health_check', datetime.now())
        
        # Monitoring thresholds
        object.__setattr__(self, '_monitoring_thresholds', {
            'max_drawdown_percent': 15.0,
            'min_win_rate': 40.0,
            'min_profit_factor': 1.2,
            'max_consecutive_losses': 5,
            'min_sharpe_ratio': 0.5
        })
    
    @property
    def trades_database(self) -> List[TradeResult]:
        return getattr(self, '_trades_database', [])
    
    @property
    def calculator(self) -> PerformanceCalculator:
        return getattr(self, '_calculator', PerformanceCalculator())
    
    @property
    def pattern_analyzer(self) -> PatternAnalyzer:
        return getattr(self, '_pattern_analyzer', PatternAnalyzer())
    
    @property
    def learning_engine(self) -> LearningEngine:
        return getattr(self, '_learning_engine', LearningEngine())
    
    @property
    def recalibration_frequency(self) -> int:
        return object.__getattribute__(self, '_recalibration_frequency') if hasattr(self, '_recalibration_frequency') else 5
    
    @property
    def last_recalibration(self) -> datetime:
        return object.__getattribute__(self, '_last_recalibration') if hasattr(self, '_last_recalibration') else datetime.now()
    
    def _run(self, action: str, data: str = "") -> str:
        """Enhanced performance analytics with additional actions"""
        try:
            # Original actions
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
            
            # Enhanced actions
            elif action == "real_time_monitor":
                return self._real_time_monitoring()
            elif action == "health_check":
                return self._system_health_check()
            elif action == "predict_performance":
                return self._predict_performance()
            elif action == "risk_analysis":
                return self._risk_analysis()
            elif action == "confluence_effectiveness":
                return self._analyze_confluence_effectiveness()
            elif action == "set_alerts":
                alert_config = json.loads(data) if data else {}
                return self._configure_alerts(alert_config)
            elif action == "benchmark":
                benchmark_data = json.loads(data) if data else {}
                return self._benchmark_analysis(benchmark_data)
            
            else:
                return f"Unknown action: {action}. Available actions: {self._get_available_actions()}"
        
        except Exception as e:
            return f"Error in enhanced performance analytics: {str(e)}"
    
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
            if len(closed_trades) % self.recalibration_frequency == 0:
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
        time_since_last = datetime.now() - self.last_recalibration
        closed_trades = len([t for t in self.trades_database if t.status == 'CLOSED'])
        
        output = []
        output.append("🔧 OPTIMIZATION STATUS")
        output.append("=" * 50)
        output.append(f"Last Recalibration: {self.last_recalibration.strftime('%Y-%m-%d %H:%M:%S')}")
        output.append(f"Time Since Last: {time_since_last}")
        output.append(f"Closed Trades: {closed_trades}")
        output.append(f"Next Recalibration: Every {self.recalibration_frequency} trades")
        
        trades_until_next = self.recalibration_frequency - (closed_trades % self.recalibration_frequency)
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
    
    def _real_time_monitoring(self) -> str:
        """Real-time performance monitoring with alerts"""
        if not self.trades_database:
            return "No trade data available for real-time monitoring"
        
        current_metrics = self.calculator.calculate_basic_metrics(self.trades_database)
        alerts = []
        
        # Check monitoring thresholds
        thresholds = getattr(self, '_monitoring_thresholds', {})
        
        if current_metrics.max_drawdown_percent > thresholds.get('max_drawdown_percent', 15):
            alerts.append(f"🚨 HIGH DRAWDOWN ALERT: {current_metrics.max_drawdown_percent:.1f}%")
        
        if current_metrics.win_rate < thresholds.get('min_win_rate', 40):
            alerts.append(f"⚠️ LOW WIN RATE ALERT: {current_metrics.win_rate:.1f}%")
        
        if current_metrics.profit_factor < thresholds.get('min_profit_factor', 1.2):
            alerts.append(f"📉 LOW PROFIT FACTOR ALERT: {current_metrics.profit_factor:.2f}")
        
        if current_metrics.max_consecutive_losses > thresholds.get('max_consecutive_losses', 5):
            alerts.append(f"🔴 CONSECUTIVE LOSSES ALERT: {current_metrics.max_consecutive_losses}")
        
        # Recent performance trend
        recent_trades = [t for t in self.trades_database if t.status == 'CLOSED'][-10:]
        if recent_trades:
            recent_pnl = [t.pnl for t in recent_trades if t.pnl is not None]
            recent_trend = "POSITIVE" if sum(recent_pnl) > 0 else "NEGATIVE"
        else:
            recent_trend = "NO_DATA"
        
        # Update real-time metrics
        current_time = datetime.now()
        real_time_data = {
            'timestamp': current_time.isoformat(),
            'current_metrics': {
                'win_rate': current_metrics.win_rate,
                'profit_factor': current_metrics.profit_factor,
                'total_pnl': current_metrics.total_pnl,
                'drawdown_percent': current_metrics.max_drawdown_percent,
                'consecutive_losses': current_metrics.max_consecutive_losses
            },
            'alerts': alerts,
            'trend': recent_trend,
            'health_score': self._calculate_health_score(current_metrics)
        }
        
        object.__setattr__(self, '_real_time_metrics', real_time_data)
        
        # Format output
        output = []
        output.append("📊 REAL-TIME PERFORMANCE MONITOR")
        output.append("=" * 50)
        output.append(f"Monitor Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
        output.append(f"Health Score: {real_time_data['health_score']:.1f}/100")
        output.append(f"Recent Trend: {recent_trend}")
        output.append("")
        
        output.append("📈 CURRENT METRICS")
        output.append("-" * 25)
        output.append(f"Win Rate: {current_metrics.win_rate:.1f}%")
        output.append(f"Profit Factor: {current_metrics.profit_factor:.2f}")
        output.append(f"Total P&L: ${current_metrics.total_pnl:.2f}")
        output.append(f"Drawdown: {current_metrics.max_drawdown_percent:.1f}%")
        output.append(f"Consecutive Losses: {current_metrics.max_consecutive_losses}")
        output.append("")
        
        if alerts:
            output.append("🚨 ACTIVE ALERTS")
            output.append("-" * 25)
            for alert in alerts:
                output.append(f"{alert}")
            output.append("")
        else:
            output.append("✅ No active alerts - System operating within parameters")
            output.append("")
        
        return "\n".join(output)
    
    def _system_health_check(self) -> str:
        """Comprehensive system health analysis"""
        if not self.trades_database:
            return "No trade data available for health check"
        
        current_metrics = self.calculator.calculate_basic_metrics(self.trades_database)
        health_components = {}
        
        # Performance health (40% weight)
        performance_score = 0
        if current_metrics.win_rate >= 60:
            performance_score += 40
        elif current_metrics.win_rate >= 50:
            performance_score += 30
        elif current_metrics.win_rate >= 40:
            performance_score += 20
        
        if current_metrics.profit_factor >= 2.0:
            performance_score += 30
        elif current_metrics.profit_factor >= 1.5:
            performance_score += 20
        elif current_metrics.profit_factor >= 1.0:
            performance_score += 10
        
        health_components['performance'] = min(performance_score, 40)
        
        # Risk management health (30% weight)
        risk_score = 30
        if current_metrics.max_drawdown_percent > 20:
            risk_score -= 15
        elif current_metrics.max_drawdown_percent > 15:
            risk_score -= 10
        elif current_metrics.max_drawdown_percent > 10:
            risk_score -= 5
        
        if current_metrics.max_consecutive_losses > 6:
            risk_score -= 10
        elif current_metrics.max_consecutive_losses > 4:
            risk_score -= 5
        
        health_components['risk_management'] = max(risk_score, 0)
        
        # Consistency health (20% weight)
        closed_trades = [t for t in self.trades_database if t.status == 'CLOSED']
        if len(closed_trades) >= 10:
            # Calculate consistency metrics
            daily_returns = []
            trade_dates = {}
            
            for trade in closed_trades:
                if trade.exit_time and trade.pnl_percent:
                    date_key = trade.exit_time.date()
                    if date_key not in trade_dates:
                        trade_dates[date_key] = []
                    trade_dates[date_key].append(trade.pnl_percent)
            
            # Daily return volatility
            for date, returns in trade_dates.items():
                daily_returns.append(sum(returns))
            
            if len(daily_returns) > 1:
                volatility = statistics.stdev(daily_returns)
                consistency_score = max(0, 20 - (volatility * 2))
            else:
                consistency_score = 15
        else:
            consistency_score = 10  # Insufficient data
        
        health_components['consistency'] = consistency_score
        
        # System optimization health (10% weight)
        optimization_history = getattr(self.learning_engine, 'optimization_history', [])
        if optimization_history:
            recent_optimization = optimization_history[-1]
            time_since_optimization = datetime.now() - recent_optimization['timestamp']
            if time_since_optimization.days < 7:
                optimization_score = 10
            elif time_since_optimization.days < 14:
                optimization_score = 7
            else:
                optimization_score = 5
        else:
            optimization_score = 5
        
        health_components['optimization'] = optimization_score
        
        # Calculate overall health score
        total_health_score = sum(health_components.values())
        
        # Health status
        if total_health_score >= 80:
            health_status = "EXCELLENT 🟢"
        elif total_health_score >= 60:
            health_status = "GOOD 🟡"
        elif total_health_score >= 40:
            health_status = "FAIR 🟠"
        else:
            health_status = "POOR 🔴"
        
        # Generate recommendations
        recommendations = []
        if health_components['performance'] < 25:
            recommendations.append("📊 Improve signal quality - Review confluence scoring weights")
        if health_components['risk_management'] < 20:
            recommendations.append("⚠️ Tighten risk management - Reduce position sizes or improve stop losses")
        if health_components['consistency'] < 15:
            recommendations.append("📈 Focus on consistency - Review trading session times and market conditions")
        if health_components['optimization'] < 8:
            recommendations.append("🔧 System needs optimization - Run parameter adjustment cycle")
        
        # Format output
        output = []
        output.append("🏥 SYSTEM HEALTH CHECK")
        output.append("=" * 50)
        output.append(f"Health Check Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output.append(f"Overall Health Score: {total_health_score:.1f}/100")
        output.append(f"Health Status: {health_status}")
        output.append("")
        
        output.append("📋 HEALTH COMPONENTS")
        output.append("-" * 30)
        output.append(f"Performance Health: {health_components['performance']:.1f}/40")
        output.append(f"Risk Management: {health_components['risk_management']:.1f}/30")
        output.append(f"Consistency: {health_components['consistency']:.1f}/20")
        output.append(f"Optimization: {health_components['optimization']:.1f}/10")
        output.append("")
        
        if recommendations:
            output.append("💡 HEALTH RECOMMENDATIONS")
            output.append("-" * 30)
            for rec in recommendations:
                output.append(f"• {rec}")
        
        # Update last health check time
        object.__setattr__(self, '_last_health_check', datetime.now())
        
        return "\n".join(output)
    
    def _predict_performance(self) -> str:
        """Predict future performance based on current trends"""
        closed_trades = [t for t in self.trades_database if t.status == 'CLOSED']
        
        if len(closed_trades) < 20:
            return "Insufficient trade history for performance prediction (minimum 20 trades required)"
        
        # Analyze recent trends
        recent_trades = closed_trades[-10:]
        older_trades = closed_trades[-20:-10] if len(closed_trades) >= 20 else closed_trades[:-10]
        
        # Calculate trend metrics
        recent_metrics = self.calculator.calculate_basic_metrics(recent_trades)
        older_metrics = self.calculator.calculate_basic_metrics(older_trades) if older_trades else recent_metrics
        
        # Trend analysis
        win_rate_trend = recent_metrics.win_rate - older_metrics.win_rate
        pf_trend = recent_metrics.profit_factor - older_metrics.profit_factor
        
        # Performance predictions for next 10 trades
        predicted_win_rate = min(95, max(5, recent_metrics.win_rate + (win_rate_trend * 0.5)))
        predicted_profit_factor = max(0.1, recent_metrics.profit_factor + (pf_trend * 0.3))
        
        # Risk predictions
        if recent_metrics.max_consecutive_losses > older_metrics.max_consecutive_losses:
            risk_level = "INCREASING"
        elif recent_metrics.max_consecutive_losses < older_metrics.max_consecutive_losses:
            risk_level = "DECREASING"
        else:
            risk_level = "STABLE"
        
        # Confidence in predictions based on data quality
        data_quality = min(100, len(closed_trades) * 2)  # More trades = higher confidence
        prediction_confidence = min(95, data_quality + (20 if abs(win_rate_trend) < 5 else 0))
        
        # Market regime analysis
        recent_returns = [t.pnl_percent for t in recent_trades if t.pnl_percent]
        if recent_returns:
            volatility = statistics.stdev(recent_returns) if len(recent_returns) > 1 else 0
            if volatility > 5:
                market_regime = "HIGH_VOLATILITY"
            elif volatility > 2:
                market_regime = "MEDIUM_VOLATILITY"
            else:
                market_regime = "LOW_VOLATILITY"
        else:
            market_regime = "UNKNOWN"
        
        predictions = {
            'next_10_trades': {
                'predicted_win_rate': predicted_win_rate,
                'predicted_profit_factor': predicted_profit_factor,
                'risk_level': risk_level,
                'market_regime': market_regime
            },
            'confidence': prediction_confidence,
            'trends': {
                'win_rate_trend': win_rate_trend,
                'profit_factor_trend': pf_trend
            }
        }
        
        object.__setattr__(self, '_predictions', predictions)
        
        # Format output
        output = []
        output.append("🔮 PERFORMANCE PREDICTIONS")
        output.append("=" * 50)
        output.append(f"Prediction Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output.append(f"Prediction Confidence: {prediction_confidence:.1f}%")
        output.append("")
        
        output.append("📊 NEXT 10 TRADES FORECAST")
        output.append("-" * 30)
        output.append(f"Predicted Win Rate: {predicted_win_rate:.1f}%")
        output.append(f"Predicted Profit Factor: {predicted_profit_factor:.2f}")
        output.append(f"Risk Level Trend: {risk_level}")
        output.append(f"Market Regime: {market_regime}")
        output.append("")
        
        output.append("📈 CURRENT TRENDS")
        output.append("-" * 30)
        trend_emoji = "📈" if win_rate_trend > 0 else "📉" if win_rate_trend < 0 else "➡️"
        output.append(f"Win Rate Trend: {trend_emoji} {win_rate_trend:+.1f}%")
        
        pf_emoji = "📈" if pf_trend > 0 else "📉" if pf_trend < 0 else "➡️"
        output.append(f"Profit Factor Trend: {pf_emoji} {pf_trend:+.2f}")
        output.append("")
        
        # Recommendations based on predictions
        recommendations = []
        if predicted_win_rate < 50:
            recommendations.append("🚨 Predicted poor performance - Consider system optimization")
        if predicted_profit_factor < 1.2:
            recommendations.append("⚠️ Low profit factor predicted - Review risk/reward ratios")
        if risk_level == "INCREASING":
            recommendations.append("📉 Increasing risk detected - Consider reducing position sizes")
        if market_regime == "HIGH_VOLATILITY":
            recommendations.append("🌊 High volatility environment - Adjust strategies accordingly")
        
        if recommendations:
            output.append("💡 PREDICTIVE RECOMMENDATIONS")
            output.append("-" * 30)
            for rec in recommendations:
                output.append(f"• {rec}")
        
        return "\n".join(output)
    
    def _analyze_confluence_effectiveness(self) -> str:
        """Detailed analysis of confluence factor effectiveness"""
        closed_trades = [t for t in self.trades_database if t.status == 'CLOSED']
        
        if len(closed_trades) < 10:
            return "Insufficient trade data for confluence analysis (minimum 10 trades required)"
        
        # Group trades by confluence score ranges
        score_ranges = {
            'High (80-100%)': [t for t in closed_trades if t.confluence_score >= 80],
            'Medium (60-79%)': [t for t in closed_trades if 60 <= t.confluence_score < 80],
            'Low (40-59%)': [t for t in closed_trades if 40 <= t.confluence_score < 60],
            'Very Low (<40%)': [t for t in closed_trades if t.confluence_score < 40]
        }
        
        # Analyze signal effectiveness
        wyckoff_trades = [t for t in closed_trades if t.wyckoff_signals]
        smc_trades = [t for t in closed_trades if t.smc_signals]
        pattern_trades = [t for t in closed_trades if t.patterns_detected]
        
        # Calculate success rates for each group
        range_analysis = {}
        for range_name, trades in score_ranges.items():
            if trades:
                wins = len([t for t in trades if t.pnl and t.pnl > 0])
                win_rate = (wins / len(trades)) * 100
                avg_pnl = sum([t.pnl for t in trades if t.pnl]) / len(trades)
                range_analysis[range_name] = {
                    'count': len(trades),
                    'win_rate': win_rate,
                    'avg_pnl': avg_pnl
                }
        
        # Signal type analysis
        signal_analysis = {}
        for signal_type, trades in [
            ('Wyckoff', wyckoff_trades),
            ('SMC', smc_trades),
            ('Patterns', pattern_trades)
        ]:
            if trades:
                wins = len([t for t in trades if t.pnl and t.pnl > 0])
                win_rate = (wins / len(trades)) * 100
                avg_pnl = sum([t.pnl for t in trades if t.pnl]) / len(trades)
                signal_analysis[signal_type] = {
                    'count': len(trades),
                    'win_rate': win_rate,
                    'avg_pnl': avg_pnl
                }
        
        # Format output
        output = []
        output.append("🎯 CONFLUENCE EFFECTIVENESS ANALYSIS")
        output.append("=" * 50)
        output.append(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output.append(f"Total Trades Analyzed: {len(closed_trades)}")
        output.append("")
        
        output.append("📊 CONFLUENCE SCORE RANGES")
        output.append("-" * 35)
        for range_name, analysis in range_analysis.items():
            if analysis['count'] > 0:
                output.append(f"{range_name}:")
                output.append(f"  Trades: {analysis['count']}")
                output.append(f"  Win Rate: {analysis['win_rate']:.1f}%")
                output.append(f"  Avg P&L: ${analysis['avg_pnl']:.2f}")
                output.append("")
        
        output.append("🔍 SIGNAL TYPE EFFECTIVENESS")
        output.append("-" * 35)
        for signal_type, analysis in signal_analysis.items():
            if analysis['count'] > 0:
                output.append(f"{signal_type} Signals:")
                output.append(f"  Trades: {analysis['count']}")
                output.append(f"  Win Rate: {analysis['win_rate']:.1f}%")
                output.append(f"  Avg P&L: ${analysis['avg_pnl']:.2f}")
                output.append("")
        
        # Recommendations for weight adjustments
        recommendations = []
        if range_analysis.get('High (80-100%)', {}).get('win_rate', 0) > 70:
            recommendations.append("✅ High confluence signals performing well - maintain current thresholds")
        elif range_analysis.get('High (80-100%)', {}).get('win_rate', 0) < 60:
            recommendations.append("⚠️ High confluence signals underperforming - review confluence calculation")
        
        best_signal = max(signal_analysis.items(), key=lambda x: x[1]['win_rate']) if signal_analysis else None
        if best_signal:
            recommendations.append(f"📈 {best_signal[0]} signals performing best - consider increasing weight")
        
        if recommendations:
            output.append("💡 OPTIMIZATION RECOMMENDATIONS")
            output.append("-" * 35)
            for rec in recommendations:
                output.append(f"• {rec}")
        
        return "\n".join(output)
    
    def _calculate_health_score(self, metrics: PerformanceMetrics) -> float:
        """Calculate overall system health score"""
        score = 0
        
        # Win rate (25 points)
        if metrics.win_rate >= 70:
            score += 25
        elif metrics.win_rate >= 60:
            score += 20
        elif metrics.win_rate >= 50:
            score += 15
        elif metrics.win_rate >= 40:
            score += 10
        
        # Profit factor (25 points)
        if metrics.profit_factor >= 2.0:
            score += 25
        elif metrics.profit_factor >= 1.5:
            score += 20
        elif metrics.profit_factor >= 1.2:
            score += 15
        elif metrics.profit_factor >= 1.0:
            score += 10
        
        # Drawdown (25 points)
        if metrics.max_drawdown_percent <= 5:
            score += 25
        elif metrics.max_drawdown_percent <= 10:
            score += 20
        elif metrics.max_drawdown_percent <= 15:
            score += 15
        elif metrics.max_drawdown_percent <= 25:
            score += 10
        
        # Risk metrics (25 points)
        risk_score = 25
        if metrics.max_consecutive_losses > 5:
            risk_score -= 10
        if metrics.sharpe_ratio < 0.5:
            risk_score -= 10
        if metrics.total_trades < 20:
            risk_score -= 5
        
        score += max(0, risk_score)
        
        return score
    
    def _default_alerts_config(self) -> Dict:
        """Default alert configuration"""
        return {
            'max_drawdown': {'threshold': 15.0, 'enabled': True},
            'consecutive_losses': {'threshold': 5, 'enabled': True},
            'win_rate_drop': {'threshold': 40.0, 'enabled': True},
            'profit_factor_drop': {'threshold': 1.2, 'enabled': True},
            'daily_loss_limit': {'threshold': -500.0, 'enabled': True}
        }
    
    def _get_available_actions(self) -> str:
        """Get list of available actions"""
        return "analyze, add_trade, optimize, report, patterns, real_time_monitor, health_check, predict_performance, risk_analysis, confluence_effectiveness, set_alerts, benchmark"

    # Additional methods for risk analysis, benchmarking, etc.
    def _risk_analysis(self) -> str: # type: ignore
        """Comprehensive risk analysis"""
        # Implementation for detailed risk analysis
        pass

    
    def _configure_alerts(self, alert_config: Dict) -> str: # type: ignore
        """Configure performance alerts"""
        # Implementation for alert configuration
        pass
    
    def _benchmark_analysis(self, benchmark_data: Dict) -> str: # type: ignore
        """Compare performance against benchmarks"""
        # Implementation for benchmark comparison
        pass