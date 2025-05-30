from datetime import timedelta
from typing import List
from data_structures.ohlc import OHLCData
from data_structures.pattern_results import PatternResult


class CandlestickPatterns:
    """Candlestick pattern recognition"""
    
    @staticmethod
    def is_doji(candle: OHLCData, threshold: float = 0.1) -> bool:
        """Check if candle is a doji (open ≈ close)"""
        body_size = abs(candle.close - candle.open)
        candle_range = candle.high - candle.low
        return (body_size / candle_range) < threshold if candle_range > 0 else False
    
    @staticmethod
    def is_hammer(candle: OHLCData) -> bool:
        """Check if candle is a hammer pattern"""
        body_size = abs(candle.close - candle.open)
        upper_shadow = candle.high - max(candle.open, candle.close)
        lower_shadow = min(candle.open, candle.close) - candle.low
        candle_range = candle.high - candle.low
        
        if candle_range == 0:
            return False
        
        return (
            lower_shadow > body_size * 2 and  # Long lower shadow
            upper_shadow < body_size * 0.5 and  # Short upper shadow
            body_size / candle_range > 0.1  # Reasonable body size
        )
    
    @staticmethod
    def is_engulfing(prev_candle: OHLCData, curr_candle: OHLCData) -> str:
        """Check for bullish/bearish engulfing pattern"""
        prev_bullish = prev_candle.close > prev_candle.open
        curr_bullish = curr_candle.close > curr_candle.open
        
        # Bullish engulfing
        if (not prev_bullish and curr_bullish and 
            curr_candle.open < prev_candle.close and 
            curr_candle.close > prev_candle.open):
            return "BULLISH_ENGULFING"
        
        # Bearish engulfing
        if (prev_bullish and not curr_bullish and 
            curr_candle.open > prev_candle.close and 
            curr_candle.close < prev_candle.open):
            return "BEARISH_ENGULFING"
        
        return "NONE"
    
    @staticmethod
    def detect_candlestick_patterns(ohlc_data: List[OHLCData]) -> List[PatternResult]:
        """Detect various candlestick patterns"""
        patterns = []
        
        for i in range(1, len(ohlc_data)):
            current = ohlc_data[i]
            previous = ohlc_data[i-1] if i > 0 else None
            
            # Doji pattern
            if CandlestickPatterns.is_doji(current):
                confidence = 70
                # Check context for higher confidence
                if i > 5:
                    recent_trend = sum([1 if ohlc_data[j].close > ohlc_data[j].open else -1 
                                      for j in range(i-5, i)])
                    if abs(recent_trend) >= 3:  # Strong trend before doji
                        confidence = 85
                
                patterns.append(PatternResult(
                    pattern_name="Doji",
                    pattern_type="CANDLESTICK",
                    direction="REVERSAL",
                    confidence=confidence,
                    start_index=i,
                    end_index=i,
                    key_levels={"doji_level": current.close},
                    target_price=None,
                    stop_loss=None,
                    formation_time=timedelta(hours=1),
                    description=f"Doji pattern at {current.close:.5f} indicates indecision",
                    reliability_score=75.0
                ))
            
            # Hammer pattern
            if CandlestickPatterns.is_hammer(current):
                # Check if at support/low
                recent_low = min([c.low for c in ohlc_data[max(0, i-10):i+1]])
                at_support = abs(current.low - recent_low) / recent_low < 0.01
                
                confidence = 75 if at_support else 60
                
                patterns.append(PatternResult(
                    pattern_name="Hammer",
                    pattern_type="CANDLESTICK", 
                    direction="BULLISH",
                    confidence=confidence,
                    start_index=i,
                    end_index=i,
                    key_levels={
                        "hammer_low": current.low,
                        "hammer_body": (current.open + current.close) / 2
                    },
                    target_price=current.close + (current.close - current.low),
                    stop_loss=current.low * 0.999,
                    formation_time=timedelta(hours=1),
                    description=f"Hammer at {current.close:.5f}, bullish reversal signal",
                    reliability_score=78.0
                ))
            
            # Engulfing patterns
            if previous:
                engulfing_type = CandlestickPatterns.is_engulfing(previous, current)
                if engulfing_type != "NONE":
                    confidence = 80
                    
                    # Check volume confirmation
                    if current.volume > previous.volume * 1.2:
                        confidence += 10
                    
                    direction = "BULLISH" if "BULLISH" in engulfing_type else "BEARISH"
                    
                    patterns.append(PatternResult(
                        pattern_name=engulfing_type.replace("_", " ").title(),
                        pattern_type="CANDLESTICK",
                        direction=direction,
                        confidence=confidence,
                        start_index=i-1,
                        end_index=i,
                        key_levels={
                            "engulfing_high": max(previous.high, current.high),
                            "engulfing_low": min(previous.low, current.low)
                        },
                        target_price=None,
                        stop_loss=None,
                        formation_time=timedelta(hours=2),
                        description=f"{engulfing_type.replace('_', ' ').title()} pattern confirmed",
                        reliability_score=82.0
                    ))
        
        return patterns