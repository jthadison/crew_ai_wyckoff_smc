from datetime import datetime
from typing import Dict, List
from data_structures.confluence_signal import ConfluenceSignal
from tools.analyzers.advanced_smc_analyzer import AdvancedSMCAnalyzer
from tools.analyzers.advanced_wyckoff_analyzer import AdvancedWyckoffAnalyzer

import numpy as np


class ConfluenceAnalyzer:
    """Analyze confluence between Wyckoff and SMC patterns"""
    
    def __init__(self):
        self.wyckoff_analyzer = AdvancedWyckoffAnalyzer()
        self.smc_analyzer = AdvancedSMCAnalyzer()
    
    def analyze_confluence(self, ohlc_data: List, technical_indicators: Dict = {}) -> ConfluenceSignal:
        """Analyze confluence between all methodologies"""
        if len(ohlc_data) < 20:
            return ConfluenceSignal(
                signal_type="NEUTRAL",
                confluence_score=0,
                entry_price=0,
                stop_loss=0,
                take_profit=0,
                risk_reward_ratio=0,
                wyckoff_patterns=[],
                smc_patterns=[],
                timestamp=datetime.now(),
                reasoning="Not enough data for confluence analysis",
                supporting_indicators=[]
            )
        
        current_price = ohlc_data[-1].close
        
        # Wyckoff analysis
        wyckoff_schematic = self.wyckoff_analyzer.detect_wyckoff_schematic(ohlc_data)
        composite_operator = self.wyckoff_analyzer.detect_composite_operator_activity(ohlc_data)
        
        # SMC analysis
        market_structure = self.smc_analyzer.detect_market_structure_shift(ohlc_data)
        order_flow = self.smc_analyzer.detect_institutional_order_flow(ohlc_data)
        
        # Score confluence
        confluence_score = 0
        signal_type = "NEUTRAL"
        wyckoff_patterns = []
        smc_patterns = []
        supporting_indicators = []
        reasoning_parts = []
        
        # Wyckoff scoring
        if wyckoff_schematic['expected_direction'] == 'BULLISH':
            confluence_score += wyckoff_schematic['confidence'] * 0.4
            signal_type = "BUY"
            wyckoff_patterns.append(f"{wyckoff_schematic['phase']} ({wyckoff_schematic['confidence']}%)")
            reasoning_parts.append(f"Wyckoff {wyckoff_schematic['phase']} phase indicates bullish bias")
        
        elif wyckoff_schematic['expected_direction'] == 'BEARISH':
            confluence_score += wyckoff_schematic['confidence'] * 0.4
            signal_type = "SELL"
            wyckoff_patterns.append(f"{wyckoff_schematic['phase']} ({wyckoff_schematic['confidence']}%)")
            reasoning_parts.append(f"Wyckoff {wyckoff_schematic['phase']} phase indicates bearish bias")
        
        # Composite operator activity scoring
        if composite_operator['detected']:
            latest_activity = composite_operator['latest_activity']
            if latest_activity:
                if 'BUYING' in latest_activity['type'] or 'ACCUMULATION' in latest_activity['type']:
                    if signal_type == "BUY":
                        confluence_score += 15  # Confirmation
                        wyckoff_patterns.append(f"Institutional {latest_activity['type']}")
                        reasoning_parts.append("Institutional buying activity detected")
                elif 'SELLING' in latest_activity['type'] or 'DISTRIBUTION' in latest_activity['type']:
                    if signal_type == "SELL":
                        confluence_score += 15  # Confirmation
                        wyckoff_patterns.append(f"Institutional {latest_activity['type']}")
                        reasoning_parts.append("Institutional selling activity detected")
        
        # SMC scoring
        if market_structure['detected']:
            for shift in market_structure['shifts']:
                if shift['type'] == 'BULLISH_BOS' and signal_type == "BUY":
                    confluence_score += shift['confidence'] * 0.3
                    smc_patterns.append(f"Bullish BOS ({shift['confidence']}%)")
                    reasoning_parts.append("Bullish break of structure confirms upward bias")
                elif shift['type'] == 'BEARISH_BOS' and signal_type == "SELL":
                    confluence_score += shift['confidence'] * 0.3
                    smc_patterns.append(f"Bearish BOS ({shift['confidence']}%)")
                    reasoning_parts.append("Bearish break of structure confirms downward bias")
        
        # Order flow scoring
        if order_flow['detected'] and order_flow['latest_signal']:
            latest_signal = order_flow['latest_signal']
            if ('BUYING' in latest_signal['type'] and signal_type == "BUY") or \
               ('SELLING' in latest_signal['type'] and signal_type == "SELL"):
                confluence_score += latest_signal['confidence'] * 0.2
                smc_patterns.append(f"Order Flow: {latest_signal['type']}")
                reasoning_parts.append(f"Recent {latest_signal['type'].lower()} detected")
        
        # Technical indicators scoring (if provided)
        if technical_indicators:
            if 'rsi' in technical_indicators:
                rsi_value = technical_indicators['rsi'].get('value')
                if rsi_value:
                    if rsi_value < 30 and signal_type == "BUY":
                        confluence_score += 10
                        supporting_indicators.append(f"RSI Oversold ({rsi_value:.1f})")
                        reasoning_parts.append("RSI oversold supports bullish bias")
                    elif rsi_value > 70 and signal_type == "SELL":
                        confluence_score += 10
                        supporting_indicators.append(f"RSI Overbought ({rsi_value:.1f})")
                        reasoning_parts.append("RSI overbought supports bearish bias")
            
            if 'macd' in technical_indicators:
                macd_data = technical_indicators['macd']
                if macd_data.get('histogram'):
                    if macd_data['histogram'] > 0 and signal_type == "BUY":
                        confluence_score += 8
                        supporting_indicators.append("MACD Bullish")
                        reasoning_parts.append("MACD histogram bullish")
                    elif macd_data['histogram'] < 0 and signal_type == "SELL":
                        confluence_score += 8
                        supporting_indicators.append("MACD Bearish")
                        reasoning_parts.append("MACD histogram bearish")
        
        # Normalize confluence score to 0-100
        confluence_score = min(100, max(0, confluence_score))
        
        # Only generate signal if confluence score is above threshold
        if confluence_score < 60:
            signal_type = "NEUTRAL"
        
        # Calculate risk management levels
        atr = self._calculate_atr(ohlc_data[-14:])  # 14-period ATR
        
        if signal_type == "BUY":
            stop_loss = current_price - (atr * 1.5)
            take_profit = current_price + (atr * 4.5)  # 1:3 risk reward
            entry_price = current_price
        elif signal_type == "SELL":
            stop_loss = current_price + (atr * 1.5)
            take_profit = current_price - (atr * 4.5)
            entry_price = current_price
        else:
            stop_loss = current_price
            take_profit = current_price
            entry_price = current_price
        
        risk_reward_ratio = abs(take_profit - entry_price) / abs(stop_loss - entry_price) if abs(stop_loss - entry_price) > 0 else 0
        
        return ConfluenceSignal(
            signal_type=signal_type,
            confluence_score=confluence_score,
            entry_price=entry_price,
            stop_loss=stop_loss,
            take_profit=take_profit,
            risk_reward_ratio=risk_reward_ratio,
            wyckoff_patterns=wyckoff_patterns,
            smc_patterns=smc_patterns,
            supporting_indicators=supporting_indicators,
            timestamp=ohlc_data[-1].timestamp,
            reasoning=". ".join(reasoning_parts) if reasoning_parts else "No significant confluence detected"
        )
    
    def _calculate_atr(self, ohlc_data: List, period: int = 14) -> float:
        """Calculate Average True Range"""
        if len(ohlc_data) < 2:
            return 0.01  # Default ATR
        
        true_ranges = []
        
        for i in range(1, len(ohlc_data)):
            current = ohlc_data[i]
            previous = ohlc_data[i-1]
            
            tr1 = current.high - current.low
            tr2 = abs(current.high - previous.close)
            tr3 = abs(current.low - previous.close)
            
            true_range = max(tr1, tr2, tr3)
            true_ranges.append(true_range)
        
        return float(np.mean(true_ranges)) if true_ranges else 0.01
    
    def get_confluence_summary(self, confluence_signal: ConfluenceSignal) -> str:
        """Format confluence analysis into readable summary"""
        if not confluence_signal:
            return "No confluence analysis available"
        
        summary = []
        summary.append(f"🎯 CONFLUENCE ANALYSIS")
        summary.append("=" * 40)
        summary.append(f"Signal: {confluence_signal.signal_type}")
        summary.append(f"Confluence Score: {confluence_signal.confluence_score:.1f}%")
        summary.append(f"Entry Price: {confluence_signal.entry_price:.5f}")
        summary.append(f"Stop Loss: {confluence_signal.stop_loss:.5f}")
        summary.append(f"Take Profit: {confluence_signal.take_profit:.5f}")
        summary.append(f"Risk:Reward Ratio: 1:{confluence_signal.risk_reward_ratio:.1f}")
        summary.append("")
        
        if confluence_signal.wyckoff_patterns:
            summary.append("🏛️ Wyckoff Patterns:")
            for pattern in confluence_signal.wyckoff_patterns:
                summary.append(f"  • {pattern}")
            summary.append("")
        
        if confluence_signal.smc_patterns:
            summary.append("💰 SMC Patterns:")
            for pattern in confluence_signal.smc_patterns:
                summary.append(f"  • {pattern}")
            summary.append("")
        
        if confluence_signal.supporting_indicators:
            summary.append("📈 Supporting Indicators:")
            for indicator in confluence_signal.supporting_indicators:
                summary.append(f"  • {indicator}")
            summary.append("")
        
        summary.append("💡 Analysis Reasoning:")
        summary.append(f"  {confluence_signal.reasoning}")
        
        return "\n".join(summary)