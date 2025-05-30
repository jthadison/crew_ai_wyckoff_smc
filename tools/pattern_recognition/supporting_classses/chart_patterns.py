from datetime import timedelta
from typing import Dict, List, Tuple

from data_structures.ohlc import OHLCData
from data_structures.pattern_results import PatternResult


class ChartPatterns:
    """Chart pattern recognition (triangles, H&S, flags, etc.)"""
    
    @staticmethod
    def find_pivot_points(ohlc_data: List[OHLCData], window: int = 5) -> Dict[str, List[Tuple[int, float]]]:
        """Find pivot highs and lows"""
        highs = [c.high for c in ohlc_data]
        lows = [c.low for c in ohlc_data]
        
        pivot_highs = []
        pivot_lows = []
        
        for i in range(window, len(ohlc_data) - window):
            # Pivot high
            if all(highs[i] >= highs[j] for j in range(i-window, i+window+1) if j != i):
                pivot_highs.append((i, highs[i]))
            
            # Pivot low
            if all(lows[i] <= lows[j] for j in range(i-window, i+window+1) if j != i):
                pivot_lows.append((i, lows[i]))
        
        return {"highs": pivot_highs, "lows": pivot_lows}
    
    @staticmethod
    def detect_triangle_patterns(ohlc_data: List[OHLCData]) -> List[PatternResult]:
        """Detect triangle patterns (ascending, descending, symmetrical)"""
        if len(ohlc_data) < 20:
            return []
        
        patterns = []
        pivot_points = ChartPatterns.find_pivot_points(ohlc_data)
        
        highs = pivot_points["highs"]
        lows = pivot_points["lows"]
        
        if len(highs) < 3 or len(lows) < 3:
            return []
        
        # Take recent pivot points
        recent_highs = highs[-5:] if len(highs) >= 5 else highs
        recent_lows = lows[-5:] if len(lows) >= 5 else lows
        
        # Calculate trend lines
        if len(recent_highs) >= 2:
            high_slope = (recent_highs[-1][1] - recent_highs[0][1]) / (recent_highs[-1][0] - recent_highs[0][0])
        else:
            high_slope = 0
            
        if len(recent_lows) >= 2:
            low_slope = (recent_lows[-1][1] - recent_lows[0][1]) / (recent_lows[-1][0] - recent_lows[0][0])
        else:
            low_slope = 0
        
        # Determine triangle type
        triangle_type = None
        direction = "NEUTRAL"
        confidence = 60
        
        if high_slope < -0.0001 and abs(low_slope) < 0.0001:  # Descending triangle
            triangle_type = "Descending Triangle"
            direction = "BEARISH"
            confidence = 75
        elif high_slope > 0.0001 and abs(low_slope) < 0.0001:  # Ascending triangle
            triangle_type = "Ascending Triangle"
            direction = "BULLISH"
            confidence = 75
        elif high_slope < -0.0001 and low_slope > 0.0001:  # Symmetrical triangle
            triangle_type = "Symmetrical Triangle"
            direction = "CONTINUATION"
            confidence = 70
        
        if triangle_type:
            start_idx = min(recent_highs[0][0], recent_lows[0][0])
            end_idx = len(ohlc_data) - 1
            
            patterns.append(PatternResult(
                pattern_name=triangle_type,
                pattern_type="CHART",
                direction=direction,
                confidence=confidence,
                start_index=start_idx,
                end_index=end_idx,
                key_levels={
                    "resistance": recent_highs[-1][1],
                    "support": recent_lows[-1][1],
                    "apex_price": (recent_highs[-1][1] + recent_lows[-1][1]) / 2
                },
                target_price=None,
                stop_loss=None,
                formation_time=timedelta(hours=(end_idx - start_idx)),
                description=f"{triangle_type} formation with {direction.lower()} bias",
                reliability_score=72.0
            ))
        
        return patterns
    
    @staticmethod
    def detect_head_and_shoulders(ohlc_data: List[OHLCData]) -> List[PatternResult]:
        """Detect head and shoulders pattern"""
        if len(ohlc_data) < 15:
            return []
        
        patterns = []
        pivot_points = ChartPatterns.find_pivot_points(ohlc_data, window=3)
        highs = pivot_points["highs"]
        
        if len(highs) < 3:
            return []
        
        # Look for H&S in recent highs
        for i in range(len(highs) - 2):
            left_shoulder = highs[i]
            head = highs[i + 1]
            right_shoulder = highs[i + 2]
            
            # Check H&S criteria
            head_higher = head[1] > left_shoulder[1] and head[1] > right_shoulder[1]
            shoulders_similar = abs(left_shoulder[1] - right_shoulder[1]) / left_shoulder[1] < 0.02
            
            if head_higher and shoulders_similar:
                # Find neckline (support between shoulders)
                start_idx = left_shoulder[0]
                end_idx = right_shoulder[0]
                lows_between = [c.low for c in ohlc_data[start_idx:end_idx+1]]
                neckline = min(lows_between)
                
                confidence = 80
                
                # Check if current price is below neckline (confirmation)
                current_price = ohlc_data[-1].close
                if current_price < neckline:
                    confidence = 90
                
                target_price = neckline - (head[1] - neckline)
                
                patterns.append(PatternResult(
                    pattern_name="Head and Shoulders",
                    pattern_type="CHART",
                    direction="BEARISH",
                    confidence=confidence,
                    start_index=start_idx,
                    end_index=end_idx,
                    key_levels={
                        "left_shoulder": left_shoulder[1],
                        "head": head[1],
                        "right_shoulder": right_shoulder[1],
                        "neckline": neckline
                    },
                    target_price=target_price,
                    stop_loss=head[1],
                    formation_time=timedelta(hours=(end_idx - start_idx)),
                    description=f"Head and Shoulders pattern, neckline at {neckline:.5f}",
                    reliability_score=85.0
                ))
        
        return patterns
    
    @staticmethod
    def detect_flag_patterns(ohlc_data: List[OHLCData]) -> List[PatternResult]:
        """Detect flag and pennant patterns"""
        if len(ohlc_data) < 15:
            return []
        
        patterns = []
        
        # Look for strong move followed by consolidation
        for i in range(10, len(ohlc_data) - 5):
            # Check for strong move (flagpole)
            flagpole_start = i - 10
            flagpole_end = i
            
            price_change = (ohlc_data[flagpole_end].close - ohlc_data[flagpole_start].close) / ohlc_data[flagpole_start].close
            
            if abs(price_change) > 0.03:  # At least 3% move
                # Check for consolidation after flagpole
                consolidation_data = ohlc_data[flagpole_end:flagpole_end+5]
                if len(consolidation_data) < 5:
                    continue
                
                consolidation_range = max([c.high for c in consolidation_data]) - min([c.low for c in consolidation_data])
                avg_price = sum([c.close for c in consolidation_data]) / len(consolidation_data)
                consolidation_percent = consolidation_range / avg_price
                
                if consolidation_percent < 0.02:  # Tight consolidation
                    flag_type = "Bull Flag" if price_change > 0 else "Bear Flag"
                    direction = "BULLISH" if price_change > 0 else "BEARISH"
                    
                    confidence = 70
                    if consolidation_percent < 0.01:  # Very tight
                        confidence = 80
                    
                    patterns.append(PatternResult(
                        pattern_name=flag_type,
                        pattern_type="CHART",
                        direction=direction,
                        confidence=confidence,
                        start_index=flagpole_start,
                        end_index=flagpole_end + 5,
                        key_levels={
                            "flagpole_start": ohlc_data[flagpole_start].close,
                            "flagpole_end": ohlc_data[flagpole_end].close,
                            "flag_high": max([c.high for c in consolidation_data]),
                            "flag_low": min([c.low for c in consolidation_data])
                        },
                        target_price=ohlc_data[flagpole_end].close + price_change * ohlc_data[flagpole_start].close,
                        stop_loss=min([c.low for c in consolidation_data]) if price_change > 0 else max([c.high for c in consolidation_data]),
                        formation_time=timedelta(hours=15),
                        description=f"{flag_type} pattern after {price_change*100:.1f}% move",
                        reliability_score=78.0
                    ))
        
        return patterns