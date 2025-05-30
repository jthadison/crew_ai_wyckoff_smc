from datetime import timedelta
from typing import Dict, List, Tuple

from data_structures.ohlc import OHLCData
from data_structures.pattern_results import PatternResult
import numpy as np

class VolumePatterns:
    """Volume-based pattern recognition"""
    
    @staticmethod
    def detect_volume_climax(ohlc_data: List[OHLCData]) -> List[PatternResult]:
        """Detect volume climax patterns"""
        if len(ohlc_data) < 20:
            return []
        
        patterns = []
        volumes = [c.volume for c in ohlc_data if c.volume > 0]
        
        if not volumes:
            return []
        
        avg_volume = np.mean(volumes[-20:])
        
        for i in range(10, len(ohlc_data)):
            current = ohlc_data[i]
            
            if current.volume > avg_volume * 3:  # Volume spike
                price_change = abs(current.close - current.open) / current.open
                
                # Check if high volume with small price movement (absorption)
                if price_change < 0.005:
                    direction = "ACCUMULATION" if current.close > current.open else "DISTRIBUTION"
                    confidence = 75
                    
                    patterns.append(PatternResult(
                        pattern_name="Volume Climax",
                        pattern_type="VOLUME",
                        direction=direction,
                        confidence=confidence,
                        start_index=i,
                        end_index=i,
                        key_levels={
                            "volume_ratio": float(current.volume / avg_volume),
                            "price_change": price_change,
                            "climax_price": current.close
                        },
                        target_price=None,
                        stop_loss=None,
                        formation_time=timedelta(hours=1),
                        description=f"Volume climax at {current.close:.5f}, {direction.lower()} likely",
                        reliability_score=80.0
                    ))
        
        return patterns