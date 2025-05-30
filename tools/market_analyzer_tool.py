from dataclasses import dataclass
from typing import Any, Dict, List
from data_structures.ohlc import OHLCData

@dataclass
class MarketAnalyzer:
    """Market structure analysis functions"""
    
    @staticmethod
    def identify_swing_points(data: List[OHLCData], window: int = 5) -> Dict[str, List[Dict[str, Any]]]:
        """Identify swing highs and lows"""
        
        if len(data) < window * 2 + 1:
            return {'swing_highs': [], 'swing_lows': []}
        
        swing_highs = []
        swing_lows = []
        
        for i in range(window, len(data) - window):
            current = data[i]
            
            # Check for swing high
            is_swing_high = True
            for j in range(i - window, i + window + 1):
                if j != i and data[j].high >= current.high:
                    is_swing_high = False
                    break
            
            if is_swing_high:
                swing_highs.append({
                    'timestamp': current.timestamp.isoformat(),
                    'price': current.high,
                    'index': i
                })
            
            # Check for swing low
            is_swing_low = True
            for j in range(i - window, i + window + 1):
                if j != i and data[j].low <= current.low:
                    is_swing_low = False
                    break
            
            if is_swing_low:
                swing_lows.append({
                    'timestamp': current.timestamp.isoformat(),
                    'price': current.low,
                    'index': i
                })
        
        return {'swing_highs': swing_highs, 'swing_lows': swing_lows}
    
    @staticmethod
    def identify_support_resistance(data: List[OHLCData], swing_points: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[float]]:
        """Identify support and resistance levels"""
        
        # Get recent price levels
        recent_highs = [point['price'] for point in swing_points['swing_highs'][-10:]]
        recent_lows = [point['price'] for point in swing_points['swing_lows'][-10:]]
        
        # Simple clustering for support/resistance
        support_levels = []
        resistance_levels = []
        
        # Group similar price levels (within 0.1% of each other)
        tolerance = 0.001  # 0.1%
        
        for low in recent_lows:
            # Check if this level is close to existing support
            is_new_level = True
            for support in support_levels:
                if abs(low - support) / support < tolerance:
                    is_new_level = False
                    break
            if is_new_level:
                support_levels.append(low)
        
        for high in recent_highs:
            # Check if this level is close to existing resistance
            is_new_level = True
            for resistance in resistance_levels:
                if abs(high - resistance) / resistance < tolerance:
                    is_new_level = False
                    break
            if is_new_level:
                resistance_levels.append(high)
        
        return {
            'support_levels': sorted(support_levels)[-5:],  # Keep top 5
            'resistance_levels': sorted(resistance_levels, reverse=True)[:5]  # Keep top 5
        }
    
    @staticmethod
    def determine_market_bias(data: List[OHLCData]) -> str:
        """Determine overall market bias"""
        
        if len(data) < 20:
            return 'neutral'
        
        recent_data = data[-20:]  # Last 20 candles
        
        # Calculate simple moving averages
        sma_short = sum(candle.close for candle in recent_data[-10:]) / 10
        sma_long = sum(candle.close for candle in recent_data) / 20
        
        current_price = data[-1].close
        
        # Determine bias
        if current_price > sma_short > sma_long:
            return 'bullish'
        elif current_price < sma_short < sma_long:
            return 'bearish'
        else:
            return 'neutral'