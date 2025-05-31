from typing import List, Optional
from data_structures.ohlc import OHLCData
from data_structures.wyckoff_pattern import WyckoffPattern
import numpy as np

class WyckoffAnalyzer:
    """Wyckoff Method pattern recognition"""
    
    @staticmethod
    def detect_accumulation_phase(ohlc_data: List[OHLCData]) -> Optional[WyckoffPattern]:
        """Detect Wyckoff accumulation phase"""
        if len(ohlc_data) < 50:
            return None
        
        closes = [candle.close for candle in ohlc_data]
        highs = [candle.high for candle in ohlc_data]
        lows = [candle.low for candle in ohlc_data]
        volumes = [candle.volume for candle in ohlc_data]
        
        # Look for selling climax (high volume, price drop)
        volume_avg = np.mean(volumes[-20:]) if volumes[-1] > 0 else 1
        recent_lows = []
        selling_climax_candidates = []
        
        for i in range(20, len(ohlc_data)):
            # High volume condition
            if volumes[i] > volume_avg * 1.5:
                # Price drop condition
                if closes[i] < closes[i-1] * 0.98:  # 2% drop
                    selling_climax_candidates.append(i)
                    recent_lows.append(lows[i])
        
        if len(selling_climax_candidates) < 3:
            return None
        
        # Check for at least 3 tests of the low
        lowest_point = min(recent_lows)
        test_count = 0
        
        for low in recent_lows:
            if abs(low - lowest_point) / lowest_point < 0.02:  # Within 2%
                test_count += 1
        
        if test_count >= 3:
            confidence = min(95, 60 + (test_count * 10))
            
            return WyckoffPattern(
                pattern_type="ACCUMULATION",
                phase="SELLING_CLIMAX_TESTED",
                confidence=confidence,
                start_time=ohlc_data[selling_climax_candidates[0]].timestamp,
                end_time=ohlc_data[-1].timestamp,
                key_levels={
                    "support": lowest_point,
                    "resistance": max([candle.high for candle in ohlc_data[-20:]]),
                    "volume_climax": max(volumes[-20:])
                },
                description=f"Accumulation pattern detected with {test_count} tests of support at {lowest_point:.4f}"
            )
        
        return None
    
    @staticmethod
    def detect_distribution_phase(ohlc_data: List[OHLCData]) -> Optional[WyckoffPattern]:
        """Detect Wyckoff distribution phase"""
        if len(ohlc_data) < 50:
            return None
        
        closes = [candle.close for candle in ohlc_data]
        highs = [candle.high for candle in ohlc_data]
        lows = [candle.low for candle in ohlc_data]
        volumes = [candle.volume for candle in ohlc_data]
        
        volume_avg = np.mean(volumes[-20:]) if volumes[-1] > 0 else 1
        recent_highs = []
        buying_climax_candidates = []
        
        for i in range(20, len(ohlc_data)):
            # High volume condition
            if volumes[i] > volume_avg * 1.5:
                # Price rise condition
                if closes[i] > closes[i-1] * 1.02:  # 2% rise
                    buying_climax_candidates.append(i)
                    recent_highs.append(highs[i])
        
        if len(buying_climax_candidates) < 3:
            return None
        
        # Check for at least 3 tests of the high
        highest_point = max(recent_highs)
        test_count = 0
        
        for high in recent_highs:
            if abs(high - highest_point) / highest_point < 0.02:  # Within 2%
                test_count += 1
        
        if test_count >= 3:
            confidence = min(95, 60 + (test_count * 10))
            
            return WyckoffPattern(
                pattern_type="DISTRIBUTION",
                phase="BUYING_CLIMAX_TESTED",
                confidence=confidence,
                start_time=ohlc_data[buying_climax_candidates[0]].timestamp,
                end_time=ohlc_data[-1].timestamp,
                key_levels={
                    "resistance": highest_point,
                    "support": min([candle.low for candle in ohlc_data[-20:]]),
                    "volume_climax": max(volumes[-20:])
                },
                description=f"Distribution pattern detected with {test_count} tests of resistance at {highest_point:.4f}"
            )
        
        return None
    
    @staticmethod
    def detect_spring(ohlc_data: List[OHLCData]) -> Optional[WyckoffPattern]:
        """Detect Wyckoff spring pattern"""
        if len(ohlc_data) < 30:
            return None
        
        lows = [candle.low for candle in ohlc_data]
        closes = [candle.close for candle in ohlc_data]
        volumes = [candle.volume for candle in ohlc_data]
        
        # Find recent support level
        support_level = min(lows[-20:])
        support_index = None
        
        for i in range(len(ohlc_data)-20, len(ohlc_data)):
            if lows[i] == support_level:
                support_index = i
                break
        
        if support_index is None:
            return None
        
        # Look for spring (break below support then quick recovery)
        for i in range(support_index + 1, len(ohlc_data)):
            if lows[i] < support_level * 0.995:  # Break below by 0.5%
                # Check for quick recovery
                if closes[i] > support_level:
                    confidence = 75
                    if volumes[i] < np.mean(volumes[-10:]):  # Low volume spring
                        confidence += 10
                    
                    return WyckoffPattern(
                        pattern_type="SPRING",
                        phase="SPRING_DETECTED",
                        confidence=confidence,
                        start_time=ohlc_data[support_index].timestamp,
                        end_time=ohlc_data[i].timestamp,
                        key_levels={
                            "support": support_level,
                            "spring_low": lows[i],
                            "entry_level": closes[i]
                        },
                        description=f"Spring detected: Break to {lows[i]:.4f}, recovery to {closes[i]:.4f}"
                    )
        
        return None