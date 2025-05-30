from typing import Dict, List
import numpy as np


class AdvancedWyckoffAnalyzer:
    """Advanced Wyckoff analysis with institutional footprint detection"""
    
    @staticmethod
    def detect_composite_operator_activity(ohlc_data: List, volume_threshold: float = 1.5) -> Dict:
        """Detect composite operator (institutional) activity"""
        if len(ohlc_data) < 20:
            return {'detected': False}
        
        closes = [c.close for c in ohlc_data]
        volumes = [c.volume for c in ohlc_data if c.volume > 0]
        highs = [c.high for c in ohlc_data]
        lows = [c.low for c in ohlc_data]
        
        if not volumes:
            return {'detected': False}
        
        avg_volume = np.mean(volumes[-20:])
        
        # Look for volume spikes with price action
        institutional_activity = []
        
        for i in range(10, len(ohlc_data)):
            current = ohlc_data[i]
            
            if current.volume > avg_volume * volume_threshold:
                # High volume detected, analyze price action
                price_change = abs(current.close - current.open) / current.open
                
                # Check for effort vs result analysis
                if price_change < 0.005:  # Less than 0.5% move on high volume
                    # Potential absorption (institutional accumulation/distribution)
                    if current.close > current.open:
                        activity_type = "ACCUMULATION_ABSORPTION"
                    else:
                        activity_type = "DISTRIBUTION_ABSORPTION"
                    
                    institutional_activity.append({
                        'type': activity_type,
                        'timestamp': current.timestamp,
                        'volume_ratio': current.volume / avg_volume,
                        'price_change': price_change,
                        'price': current.close
                    })
                
                elif price_change > 0.01:  # Greater than 1% move
                    # Potential institutional move
                    if current.close > current.open:
                        activity_type = "INSTITUTIONAL_BUYING"
                    else:
                        activity_type = "INSTITUTIONAL_SELLING"
                    
                    institutional_activity.append({
                        'type': activity_type,
                        'timestamp': current.timestamp,
                        'volume_ratio': current.volume / avg_volume,
                        'price_change': price_change,
                        'price': current.close
                    })
        
        return {
            'detected': len(institutional_activity) > 0,
            'activities': institutional_activity,
            'total_activities': len(institutional_activity),
            'latest_activity': institutional_activity[-1] if institutional_activity else None
        }
    
    @staticmethod
    def detect_wyckoff_schematic(ohlc_data: List) -> Dict:
        """Detect complete Wyckoff accumulation/distribution schematic"""
        if len(ohlc_data) < 100:
            return {'phase': 'INSUFFICIENT_DATA'}
        
        closes = [c.close for c in ohlc_data]
        volumes = [c.volume for c in ohlc_data if c.volume > 0]
        highs = [c.high for c in ohlc_data]
        lows = [c.low for c in ohlc_data]
        
        # Calculate price and volume characteristics
        price_range = max(closes) - min(closes)
        price_volatility = np.std(closes[-50:]) / np.mean(closes[-50:])
        
        if not volumes:
            volume_pattern = "NO_VOLUME_DATA"
        else:
            recent_vol_avg = np.mean(volumes[-20:])
            early_vol_avg = np.mean(volumes[:20])
            volume_pattern = "INCREASING" if recent_vol_avg > early_vol_avg * 1.2 else "DECREASING" if recent_vol_avg < early_vol_avg * 0.8 else "STABLE"
        
        # Determine current Wyckoff phase
        current_price = closes[-1]
        price_position = (current_price - min(closes)) / price_range
        
        # Phase determination logic
        if price_volatility < 0.02 and volume_pattern in ["STABLE", "DECREASING"]:
            if price_position < 0.3:
                phase = "ACCUMULATION"
                confidence = 75
                expected_direction = "BULLISH"
            elif price_position > 0.7:
                phase = "DISTRIBUTION"
                confidence = 75
                expected_direction = "BEARISH"
            else:
                phase = "CONSOLIDATION"
                confidence = 60
                expected_direction = "NEUTRAL"
        elif volume_pattern == "INCREASING":
            if price_position > 0.5:
                phase = "MARKUP"
                confidence = 80
                expected_direction = "BULLISH"
            else:
                phase = "MARKDOWN"
                confidence = 80
                expected_direction = "BEARISH"
        else:
            phase = "TRANSITION"
            confidence = 50
            expected_direction = "NEUTRAL"
        
        return {
            'phase': phase,
            'confidence': confidence,
            'expected_direction': expected_direction,
            'price_position': price_position,
            'volume_pattern': volume_pattern,
            'price_volatility': price_volatility,
            'analysis_summary': f"{phase} phase detected with {confidence}% confidence, expecting {expected_direction} movement"
        }