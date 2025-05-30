from typing import Dict, List
import numpy as np


class AdvancedSMCAnalyzer:
    """Advanced Smart Money Concepts analysis"""
    
    @staticmethod
    def detect_market_structure_shift(ohlc_data: List) -> Dict:
        """Detect Break of Structure (BOS) and Change of Character (CHOCH)"""
        if len(ohlc_data) < 20:
            return {'detected': False}
        
        highs = [c.high for c in ohlc_data]
        lows = [c.low for c in ohlc_data]
        closes = [c.close for c in ohlc_data]
        
        # Find recent swing highs and lows
        swing_highs = []
        swing_lows = []
        
        for i in range(5, len(ohlc_data) - 5):
            # Swing high detection
            if all(highs[i] >= highs[j] for j in range(i-5, i+6) if j != i):
                swing_highs.append({'index': i, 'price': highs[i], 'timestamp': ohlc_data[i].timestamp})
            
            # Swing low detection
            if all(lows[i] <= lows[j] for j in range(i-5, i+6) if j != i):
                swing_lows.append({'index': i, 'price': lows[i], 'timestamp': ohlc_data[i].timestamp})
        
        if len(swing_highs) < 2 or len(swing_lows) < 2:
            return {'detected': False}
        
        # Check for BOS/CHOCH
        structure_shifts = []
        current_price = closes[-1]
        
        # Recent swing points
        recent_high = swing_highs[-1] if swing_highs else None
        recent_low = swing_lows[-1] if swing_lows else None
        prev_high = swing_highs[-2] if len(swing_highs) > 1 else None
        prev_low = swing_lows[-2] if len(swing_lows) > 1 else None
        
        # Bullish BOS: Current price breaks above previous swing high
        if recent_high and prev_high and current_price > prev_high['price'] * 1.001:
            structure_shifts.append({
                'type': 'BULLISH_BOS',
                'confidence': 85,
                'break_level': prev_high['price'],
                'current_price': current_price,
                'description': f"Bullish BOS: Price broke above {prev_high['price']:.5f}"
            })
        
        # Bearish BOS: Current price breaks below previous swing low
        if recent_low and prev_low and current_price < prev_low['price'] * 0.999:
            structure_shifts.append({
                'type': 'BEARISH_BOS',
                'confidence': 85,
                'break_level': prev_low['price'],
                'current_price': current_price,
                'description': f"Bearish BOS: Price broke below {prev_low['price']:.5f}"
            })
        
        return {
            'detected': len(structure_shifts) > 0,
            'shifts': structure_shifts,
            'swing_highs': swing_highs[-3:],  # Recent swing highs
            'swing_lows': swing_lows[-3:],    # Recent swing lows
        }
    
    @staticmethod
    def detect_institutional_order_flow(ohlc_data: List) -> Dict:
        """Detect institutional order flow patterns"""
        if len(ohlc_data) < 30:
            return {'detected': False}
        
        volumes = [c.volume for c in ohlc_data if c.volume > 0]
        closes = [c.close for c in ohlc_data]
        opens = [c.open for c in ohlc_data]
        
        if not volumes:
            return {'detected': False}
        
        order_flow_signals = []
        
        for i in range(10, len(ohlc_data) - 5):
            current = ohlc_data[i]
            
            # Volume analysis
            avg_volume = np.mean(volumes[max(0, i-10):i])
            volume_ratio = current.volume / avg_volume if avg_volume > 0 else 1
            
            # Price action analysis
            body_size = abs(current.close - current.open)
            candle_range = current.high - current.low
            body_ratio = body_size / candle_range if candle_range > 0 else 0
            
            # Detect potential institutional activity
            if volume_ratio > 2.0 and body_ratio > 0.7:  # High volume, strong directional move
                if current.close > current.open:
                    order_flow_type = "INSTITUTIONAL_BUYING"
                    confidence = min(90, 60 + (volume_ratio * 10))
                else:
                    order_flow_type = "INSTITUTIONAL_SELLING"
                    confidence = min(90, 60 + (volume_ratio * 10))
                
                order_flow_signals.append({
                    'type': order_flow_type,
                    'confidence': confidence,
                    'timestamp': current.timestamp,
                    'price': current.close,
                    'volume_ratio': volume_ratio,
                    'body_ratio': body_ratio
                })
            
            # Detect absorption (high volume, small price movement)
            elif volume_ratio > 1.8 and body_ratio < 0.3:
                order_flow_signals.append({
                    'type': "ABSORPTION",
                    'confidence': 70,
                    'timestamp': current.timestamp,
                    'price': current.close,
                    'volume_ratio': volume_ratio,
                    'description': "Potential institutional absorption detected"
                })
        
        return {
            'detected': len(order_flow_signals) > 0,
            'signals': order_flow_signals,
            'total_signals': len(order_flow_signals),
            'latest_signal': order_flow_signals[-1] if order_flow_signals else None
        }