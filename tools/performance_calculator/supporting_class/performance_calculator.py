from collections import defaultdict
import math
import statistics
from typing import Dict, List, Tuple
from data_structures.performance_metrics import PerformanceMetrics
from data_structures.trade_results import TradeResult


class PerformanceCalculator:
    """Calculate various performance metrics"""
    
    @staticmethod
    def calculate_basic_metrics(trades: List[TradeResult]) -> PerformanceMetrics:
        """Calculate basic performance metrics"""
        if not trades:
            return PerformanceMetrics(
                total_trades=0, 
                winning_trades=0, 
                losing_trades=0,
                win_rate=0, 
                profit_factor=0, 
                total_pnl=0, 
                total_pnl_percent=0,
                avg_win=0, 
                avg_loss=0, 
                largest_win=0, 
                largest_loss=0,
                max_consecutive_wins=0, max_consecutive_losses=0,
                max_drawdown=0, max_drawdown_percent=0,
                sharpe_ratio=0, sortino_ratio=0, calmar_ratio=0,
                avg_trade_duration_hours=0, avg_risk_reward=0,
                expectancy=0, recovery_factor=0,
                profit_factor_by_asset={}, performance_by_timeframe={}
            )
        
        closed_trades = [t for t in trades if t.status == 'CLOSED' and t.pnl is not None]
        
        if not closed_trades:
            return PerformanceMetrics(
                total_trades=len(trades), winning_trades=0, losing_trades=0,
                win_rate=0, profit_factor=0, total_pnl=0, total_pnl_percent=0,
                avg_win=0, avg_loss=0, largest_win=0, largest_loss=0,
                max_consecutive_wins=0, max_consecutive_losses=0,
                max_drawdown=0, max_drawdown_percent=0,
                sharpe_ratio=0, sortino_ratio=0, calmar_ratio=0,
                avg_trade_duration_hours=0, avg_risk_reward=0,
                expectancy=0, recovery_factor=0,
                profit_factor_by_asset={}, performance_by_timeframe={}
            )
        
        # Basic calculations
        total_trades = len(closed_trades)
        winning_trades = len([t for t in closed_trades if t.pnl is not None and t.pnl > 0])
        losing_trades = len([t for t in closed_trades if t.pnl is not None and t.pnl < 0])
        
        win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
        
        total_pnl = sum([t.pnl for t in closed_trades if t.pnl is not None])
        total_pnl_percent = sum([t.pnl_percent for t in closed_trades if t.pnl_percent])
        
        wins = [t.pnl for t in closed_trades if t.pnl is not None and t.pnl > 0]
        losses = [abs(t.pnl) for t in closed_trades if t.pnl is not None and t.pnl < 0]
        
        avg_win = statistics.mean(wins) if wins else 0
        avg_loss = statistics.mean(losses) if losses else 0
        largest_win = max(wins) if wins else 0
        largest_loss = max(losses) if losses else 0
        
        # Profit factor
        gross_profit = sum(wins)
        gross_loss = sum(losses)
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
        
        # Consecutive wins/losses
        max_consecutive_wins = PerformanceCalculator._calculate_max_consecutive(closed_trades, True)
        max_consecutive_losses = PerformanceCalculator._calculate_max_consecutive(closed_trades, False)
        
        # Drawdown
        max_drawdown, max_drawdown_percent = PerformanceCalculator._calculate_drawdown(closed_trades)
        
        # Risk-adjusted metrics
        returns = [t.pnl_percent for t in closed_trades if t.pnl_percent]
        sharpe_ratio = PerformanceCalculator._calculate_sharpe_ratio(returns)
        sortino_ratio = PerformanceCalculator._calculate_sortino_ratio(returns)
        calmar_ratio = (total_pnl_percent / max_drawdown_percent) if max_drawdown_percent > 0 else 0
        
        # Trade duration
        durations = [t.hold_time_hours for t in closed_trades if t.hold_time_hours]
        avg_trade_duration_hours = statistics.mean(durations) if durations else 0
        
        # Risk-reward
        risk_rewards = [t.risk_reward_ratio for t in closed_trades if t.risk_reward_ratio]
        avg_risk_reward = statistics.mean(risk_rewards) if risk_rewards else 0
        
        # Expectancy
        expectancy = (win_rate/100 * avg_win) - ((100-win_rate)/100 * avg_loss)
        
        # Recovery factor
        recovery_factor = total_pnl / max_drawdown if max_drawdown > 0 else 0
        
        # Performance by asset
        profit_factor_by_asset = PerformanceCalculator._calculate_performance_by_asset(closed_trades)
        
        # Performance by timeframe
        performance_by_timeframe = PerformanceCalculator._calculate_performance_by_timeframe(closed_trades)
        
        return PerformanceMetrics(
            total_trades=total_trades,
            winning_trades=winning_trades,
            losing_trades=losing_trades,
            win_rate=win_rate,
            profit_factor=profit_factor,
            total_pnl=total_pnl,
            total_pnl_percent=total_pnl_percent,
            avg_win=avg_win,
            avg_loss=avg_loss,
            largest_win=largest_win,
            largest_loss=largest_loss,
            max_consecutive_wins=max_consecutive_wins,
            max_consecutive_losses=max_consecutive_losses,
            max_drawdown=max_drawdown,
            max_drawdown_percent=max_drawdown_percent,
            sharpe_ratio=sharpe_ratio,
            sortino_ratio=sortino_ratio,
            calmar_ratio=calmar_ratio,
            avg_trade_duration_hours=avg_trade_duration_hours,
            avg_risk_reward=avg_risk_reward,
            expectancy=expectancy,
            recovery_factor=recovery_factor,
            profit_factor_by_asset=profit_factor_by_asset,
            performance_by_timeframe=performance_by_timeframe
        )
    
    @staticmethod
    def _calculate_max_consecutive(trades: List[TradeResult], winning: bool) -> int:
        """Calculate maximum consecutive wins or losses"""
        max_consecutive = 0
        current_consecutive = 0
        
        for trade in trades:
            if trade.pnl is not None and ((winning and trade.pnl > 0) or (not winning and trade.pnl <= 0)):
                current_consecutive += 1
                max_consecutive = max(max_consecutive, current_consecutive)
            else:
                current_consecutive = 0
        
        return max_consecutive
    
    @staticmethod
    def _calculate_drawdown(trades: List[TradeResult]) -> Tuple[float, float]:
        """Calculate maximum drawdown in absolute and percentage terms"""
        if not trades:
            return 0, 0
        
        cumulative_pnl = 0
        peak_pnl = 0
        max_dd_absolute = 0
        max_dd_percent = 0
        
        for trade in trades:
            if trade.pnl is not None:
                cumulative_pnl += trade.pnl
                peak_pnl = max(peak_pnl, cumulative_pnl)
                
                drawdown = peak_pnl - cumulative_pnl
                max_dd_absolute = max(max_dd_absolute, drawdown)
                
                if peak_pnl > 0:
                    dd_percent = (drawdown / peak_pnl) * 100
                    max_dd_percent = max(max_dd_percent, dd_percent)
        
        return max_dd_absolute, max_dd_percent
    
    @staticmethod
    def _calculate_sharpe_ratio(returns: List[float], risk_free_rate: float = 0.02) -> float:
        """Calculate Sharpe ratio"""
        if not returns or len(returns) < 2:
            return 0
        
        excess_returns = [r - risk_free_rate/252 for r in returns]  # Daily risk-free rate
        mean_excess_return = statistics.mean(excess_returns)
        std_excess_return = statistics.stdev(excess_returns)
        
        return (mean_excess_return / std_excess_return) * math.sqrt(252) if std_excess_return > 0 else 0
    
    @staticmethod
    def _calculate_sortino_ratio(returns: List[float], risk_free_rate: float = 0.02) -> float:
        """Calculate Sortino ratio (only considers downside deviation)"""
        if not returns or len(returns) < 2:
            return 0
        
        excess_returns = [r - risk_free_rate/252 for r in returns]
        mean_excess_return = statistics.mean(excess_returns)
        
        negative_returns = [r for r in excess_returns if r < 0]
        if not negative_returns:
            return float('inf') if mean_excess_return > 0 else 0
        
        downside_deviation = math.sqrt(statistics.mean([r**2 for r in negative_returns]))
        
        return (mean_excess_return / downside_deviation) * math.sqrt(252) if downside_deviation > 0 else 0
    
    @staticmethod
    def _calculate_performance_by_asset(trades: List[TradeResult]) -> Dict[str, float]:
        """Calculate profit factor by asset"""
        asset_performance = defaultdict(lambda: {'wins': 0.0, 'losses': 0.0})
        
        for trade in trades:
            if trade.pnl is not None and trade.pnl > 0:
                asset_performance[trade.symbol]['wins'] += trade.pnl
            elif trade.pnl is not None:
                asset_performance[trade.symbol]['losses'] += abs(trade.pnl)
        
        profit_factors = {}
        for asset, perf in asset_performance.items():
            if perf['losses'] > 0:
                profit_factors[asset] = perf['wins'] / perf['losses']
            else:
                profit_factors[asset] = float('inf') if perf['wins'] > 0 else 0
        
        return profit_factors
    
    @staticmethod
    def _calculate_performance_by_timeframe(trades: List[TradeResult]) -> Dict[str, Dict]:
        """Calculate performance metrics by timeframe"""
        tf_performance = defaultdict(list)
        
        for trade in trades:
            tf_performance[trade.timeframe].append(trade)
        
        result = {}
        for tf, tf_trades in tf_performance.items():
            if tf_trades:
                wins = [t for t in tf_trades if t.pnl > 0]
                total_pnl = sum([t.pnl for t in tf_trades])
                win_rate = (len(wins) / len(tf_trades)) * 100
                
                result[tf] = {
                    'total_trades': len(tf_trades),
                    'win_rate': win_rate,
                    'total_pnl': total_pnl,
                    'avg_pnl': total_pnl / len(tf_trades)
                }
        
        return result