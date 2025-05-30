from datetime import timedelta
from typing import Dict, List, Tuple

from data_structures.ohlc import OHLCData
from data_structures.pattern_results import PatternResult
from tools.pattern_recognition.supporting_classses.chart_patterns import ChartPatterns

class HarmonicPatterns:
    """Harmonic pattern recognition (Gartley, Butterfly, etc.)"""
    
    @staticmethod
    def calculate_fibonacci_ratios(point_a: float, point_b: float, point_c: float) -> Dict[str, float]:
        """Calculate Fibonacci retracement/extension ratios"""
        ab_range = abs(point_b - point_a)
        bc_range = abs(point_c - point_b)
        ac_range = abs(point_c - point_a)
        
        if ab_range == 0:
            return {}
        
        return {
            "bc_to_ab": bc_range / ab_range,
            "ac_to_ab": ac_range / ab_range
        }
    
    @staticmethod
    def detect_gartley_pattern(ohlc_data: List[OHLCData]) -> List[PatternResult]:
        """Detect Gartley harmonic pattern"""
        if len(ohlc_data) < 20:
            return []
        
        patterns = []
        pivot_points = ChartPatterns.find_pivot_points(ohlc_data, window=3)
        
        # Need at least 4 pivot points for XABCD pattern
        all_pivots = []
        for idx, price in pivot_points["highs"]:
            all_pivots.append((idx, price, "HIGH"))
        for idx, price in pivot_points["lows"]:
            all_pivots.append((idx, price, "LOW"))
        
        all_pivots.sort(key=lambda x: x[0])  # Sort by index
        
        if len(all_pivots) < 4:
            return []
        
        # Check recent 4-5 pivot points for Gartley
        for i in range(len(all_pivots) - 3):
            x = all_pivots[i]
            a = all_pivots[i + 1]
            b = all_pivots[i + 2]
            c = all_pivots[i + 3]
            
            # Check if pattern alternates (high-low-high-low or low-high-low-high)
            if x[2] == a[2] or a[2] == b[2] or b[2] == c[2]:
                continue
            
            # Calculate ratios
            xa_range = abs(a[1] - x[1])
            ab_range = abs(b[1] - a[1])
            bc_range = abs(c[1] - b[1])
            
            if xa_range == 0 or ab_range == 0:
                continue
            
            ab_to_xa = ab_range / xa_range
            bc_to_ab = bc_range / ab_range
            
            # Gartley ratios: AB=0.618 XA, BC=0.382-0.886 AB
            if (0.55 <= ab_to_xa <= 0.68 and 0.35 <= bc_to_ab <= 0.90):
                # Potential Gartley pattern
                confidence = 60
                
                # Check how close to ideal ratios
                ideal_ab_xa = abs(ab_to_xa - 0.618)
                if ideal_ab_xa < 0.05:
                    confidence += 15
                
                direction = "BULLISH" if x[1] < c[1] else "BEARISH"
                
                patterns.append(PatternResult(
                    pattern_name="Gartley Pattern",
                    pattern_type="HARMONIC",
                    direction=direction,
                    confidence=confidence,
                    start_index=x[0],
                    end_index=c[0],
                    key_levels={
                        "X": x[1],
                        "A": a[1],
                        "B": b[1],
                        "C": c[1],
                        "AB_XA_ratio": ab_to_xa,
                        "BC_AB_ratio": bc_to_ab
                    },
                    target_price=None,
                    stop_loss=None,
                    formation_time=timedelta(hours=(c[0] - x[0])),
                    description=f"Gartley pattern XABCD, AB/XA={ab_to_xa:.3f}, BC/AB={bc_to_ab:.3f}",
                    reliability_score=70.0
                ))
        
        return patterns