from typing import List, Optional

from data_structures.ohlc import OHLCData
from data_structures.wyckoff_pattern import WyckoffPattern
import numpy as np
import pandas as pd

class WyckoffAnalyzer:
    """Advanced Wyckoff method analysis"""
    
    def __init__(self):
        self.phase_patterns = {
            'accumulation': self._detect_accumulation_pattern,
            'distribution': self._detect_distribution_pattern,
            'markup': self._detect_markup_pattern,
            'markdown': self._detect_markdown_pattern
        }
    
    def analyze_market_phase(self, data: List[OHLCData], volume_data: Optional[List[float]] = None) -> List[WyckoffPattern]:
        """Identify current Wyckoff market phase"""
        
        if len(data) < 50:
            return []
        
        phases = []
        
        # Analyze for each phase type
        for phase_type, detector in self.phase_patterns.items():
            detected_phases = detector(data, volume_data)
            phases.extend(detected_phases)
        
        # Sort by confidence and recency
        phases.sort(key=lambda x: (x.confidence, x.end_time or x.start_time), reverse=True)
        
        return phases
    
    def _detect_accumulation_pattern(self, data: List[OHLCData], volume_data: Optional[List[float]]) -> List[WyckoffPattern]:
        """Detect Wyckoff accumulation phase"""
        
        phases = []
        
        # Look for sideways price action with specific characteristics
        for i in range(20, len(data) - 20):
            window = data[i-20:i+20]
            
            # Calculate price range and volatility
            prices = [candle.close for candle in window]
            price_range = max(prices) - min(prices)
            avg_price = sum(prices) / len(prices)
            volatility = np.std(prices)
            
            # Look for tight range (low volatility)
            if volatility / avg_price < 0.02:  # Less than 2% volatility
                
                # Check for multiple tests of support
                lows = [candle.low for candle in window]
                support_level = min(lows)
                support_tests = sum(1 for low in lows if abs(low - support_level) / support_level < 0.005)
                
                if support_tests >= 3:  # At least 3 tests
                    
                    # Look for spring pattern (break below then recovery)
                    recent_data = data[i:i+10] if i+10 < len(data) else data[i:]
                    spring_detected = False
                    
                    for candle in recent_data:
                        if candle.low < support_level * 0.999:  # Break below support
                            # Check for recovery
                            recovery_candles = [c for c in recent_data if c.timestamp > candle.timestamp]
                            if recovery_candles and recovery_candles[-1].close > support_level:
                                spring_detected = True
                                break
                    
                    confidence = 0.6 + (support_tests * 0.1) + (0.2 if spring_detected else 0)
                    
                    if confidence > 0.7:
                        phases.append(WyckoffPattern(
                            pattern_type='accumulation',
                            phase='accumulation',
                            start_time=window[0].timestamp,
                            end_time=window[-1].timestamp,
                            key_levels={'spring_pattern': 1.0} if spring_detected else {'multiple_support_tests': 1.0},
                            confidence=confidence,
                            description='Sideways price action with multiple support tests' + (' and spring pattern' if spring_detected else ''),
                        ))
        
        return phases
    
    def _detect_distribution_pattern(self, data: List[OHLCData], volume_data: Optional[List[float]]) -> List[WyckoffPattern]:
        """Detect Wyckoff distribution phase"""
        
        phases = []
        
        # Look for sideways price action at highs with specific characteristics
        for i in range(20, len(data) - 20):
            window = data[i-20:i+20]
            
            # Calculate price range and position
            prices = [candle.close for candle in window]
            highs = [candle.high for candle in window]
            
            price_range = max(prices) - min(prices)
            avg_price = sum(prices) / len(prices)
            volatility = np.std(prices)
            
            # Look for sideways action at relatively high prices
            if volatility / avg_price < 0.025:  # Slightly higher volatility than accumulation
                
                # Check for multiple tests of resistance
                resistance_level = max(highs)
                resistance_tests = sum(1 for high in highs if abs(high - resistance_level) / resistance_level < 0.005)
                
                if resistance_tests >= 3:  # At least 3 tests
                    
                    # Look for upthrust pattern (break above then decline)
                    recent_data = data[i:i+10] if i+10 < len(data) else data[i:]
                    upthrust_detected = False
                    
                    for candle in recent_data:
                        if candle.high > resistance_level * 1.001:  # Break above resistance
                            # Check for decline
                            decline_candles = [c for c in recent_data if c.timestamp > candle.timestamp]
                            if decline_candles and decline_candles[-1].close < resistance_level:
                                upthrust_detected = True
                                break
                    
                    confidence = 0.6 + (resistance_tests * 0.1) + (0.2 if upthrust_detected else 0)
                    
                    if confidence > 0.7:
                        phases.append(WyckoffPattern(
                            pattern_type='distribution',
                            phase='distribution',
                            start_time=window[0].timestamp,
                            end_time=window[-1].timestamp,
                            key_levels={'upthrust_pattern': 1.0} if upthrust_detected else {'multiple_resistance_tests': 1.0},
                            confidence=confidence,
                            description='Sideways price action at highs with multiple resistance tests' + (' and upthrust pattern' if upthrust_detected else '')
                        ))
        
        return phases
    
    def _detect_markup_pattern(self, data: List[OHLCData], volume_data: Optional[List[float]]) -> List[WyckoffPattern]:
        """Detect Wyckoff markup phase"""
        
        phases = []
        
        # Look for sustained uptrend with higher highs and higher lows
        for i in range(30, len(data)):
            window = data[i-30:i]
            
            prices = [candle.close for candle in window]
            
            # Check for uptrend characteristics
            first_half = prices[:15]
            second_half = prices[15:]
            
            if np.mean(second_half) > np.mean(first_half) * 1.02:  # At least 2% gain
                
                # Look for higher highs and higher lows pattern
                highs = [candle.high for candle in window]
                lows = [candle.low for candle in window]
                
                recent_highs = highs[-10:]
                recent_lows = lows[-10:]
                
                higher_highs = sum(1 for j in range(1, len(recent_highs)) if recent_highs[j] > recent_highs[j-1])
                higher_lows = sum(1 for j in range(1, len(recent_lows)) if recent_lows[j] > recent_lows[j-1])
                
                if higher_highs >= 6 and higher_lows >= 6:  # Strong uptrend
                    confidence = 0.7 + (higher_highs + higher_lows) * 0.01
                    
                    phases.append(WyckoffPattern(
                        pattern_type='markup',
                        start_time=window[0].timestamp,
                        end_time=window[-1].timestamp,
                        #price_range=(min(prices), max(prices)),
                        #volume_characteristics={'trend_strength': higher_highs + higher_lows},
                        key_levels={'sustained_uptrend': 1.0, 'higher_highs_lows': 1.0},
                        confidence=min(confidence, 1.0),
                        phase='MARKUP', #higher_highs + higher_lows,
                        description='Sustained uptrend with higher highs and higher lows'
                    ))
        
        return phases
    
    def _detect_markdown_pattern(self, data: List[OHLCData], volume_data: Optional[List[float]]) -> List[WyckoffPattern]:
        """Detect Wyckoff markdown phase"""
        
        phases = []
        
        # Look for sustained downtrend with lower highs and lower lows
        for i in range(30, len(data)):
            window = data[i-30:i]
            
            prices = [candle.close for candle in window]
            
            # Check for downtrend characteristics
            first_half = prices[:15]
            second_half = prices[15:]
            
            if np.mean(second_half) < np.mean(first_half) * 0.98:  # At least 2% decline
                
                # Look for lower highs and lower lows pattern
                highs = [candle.high for candle in window]
                lows = [candle.low for candle in window]
                
                recent_highs = highs[-10:]
                recent_lows = lows[-10:]
                
                lower_highs = sum(1 for j in range(1, len(recent_highs)) if recent_highs[j] < recent_highs[j-1])
                lower_lows = sum(1 for j in range(1, len(recent_lows)) if recent_lows[j] < recent_lows[j-1])
                
                if lower_highs >= 6 and lower_lows >= 6:  # Strong downtrend
                    confidence = 0.7 + (lower_highs + lower_lows) * 0.01
                    
                    phases.append(WyckoffPattern(
                        pattern_type='markdown',
                        phase='markdown',
                        start_time=window[0].timestamp,
                        end_time=window[-1].timestamp,
                        key_levels={
                            'max_high': max(highs),
                            'min_low': min(lows)
                        },
                        description='Sustained downtrend with lower highs and lower lows',
                        confidence=min(confidence, 1.0)
                    ))
        
        return phases