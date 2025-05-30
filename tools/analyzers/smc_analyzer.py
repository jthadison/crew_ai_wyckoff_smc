from typing import List
from data_structures.ohlc import OHLCData
from data_structures.smc_pattern import SMCPattern
import numpy as np

class SMCAnalyzer:
    """Smart Money Concepts pattern recognition"""
    
    @staticmethod
    def detect_order_blocks(ohlc_data: List[OHLCData]) -> List[SMCPattern]:
        """Detect institutional order blocks"""
        if len(ohlc_data) < 20:
            return []
        
        order_blocks = []
        
        for i in range(10, len(ohlc_data) - 5):
            current = ohlc_data[i]
            
            # Bullish order block: Strong move up after consolidation
            if current.close > current.open * 1.01:  # 1% green candle
                # Check if next few candles move away from this area
                moved_away = True
                for j in range(i + 1, min(i + 6, len(ohlc_data))):
                    if ohlc_data[j].low <= current.high:
                        moved_away = False
                        break
                
                if moved_away:
                    confidence = 70
                    if current.volume > np.mean([c.volume for c in ohlc_data[i-5:i]]) * 1.5:
                        confidence += 15  # High volume confirmation
                    
                    order_blocks.append(SMCPattern(
                        pattern_type="ORDER_BLOCK",
                        direction="BULLISH",
                        confidence=confidence,
                        price_level=(current.open + current.close) / 2,
                        timestamp=current.timestamp,
                        zone_high=current.high,
                        zone_low=current.open,
                        description=f"Bullish order block: {current.open:.4f} - {current.high:.4f}"
                    ))
            
            # Bearish order block: Strong move down after consolidation
            elif current.close < current.open * 0.99:  # 1% red candle
                moved_away = True
                for j in range(i + 1, min(i + 6, len(ohlc_data))):
                    if ohlc_data[j].high >= current.low:
                        moved_away = False
                        break
                
                if moved_away:
                    confidence = 70
                    if current.volume > np.mean([c.volume for c in ohlc_data[i-5:i]]) * 1.5:
                        confidence += 15
                    
                    order_blocks.append(SMCPattern(
                        pattern_type="ORDER_BLOCK",
                        direction="BEARISH",
                        confidence=confidence,
                        price_level=(current.open + current.close) / 2,
                        timestamp=current.timestamp,
                        zone_high=current.open,
                        zone_low=current.low,
                        description=f"Bearish order block: {current.low:.4f} - {current.open:.4f}"
                    ))
        
        return order_blocks
    
    @staticmethod
    def detect_fair_value_gaps(ohlc_data: List[OHLCData]) -> List[SMCPattern]:
        """Detect Fair Value Gaps (FVG)"""
        if len(ohlc_data) < 3:
            return []
        
        fvgs = []
        
        for i in range(1, len(ohlc_data) - 1):
            prev_candle = ohlc_data[i - 1]
            current_candle = ohlc_data[i]
            next_candle = ohlc_data[i + 1]
            
            # Bullish FVG: Gap between previous high and next low
            if (prev_candle.high < next_candle.low and 
                current_candle.close > current_candle.open):
                
                gap_size = next_candle.low - prev_candle.high
                gap_percentage = gap_size / prev_candle.high * 100
                
                if gap_percentage > 0.1:  # Minimum 0.1% gap
                    confidence = min(90, 50 + gap_percentage * 10)
                    
                    fvgs.append(SMCPattern(
                        pattern_type="FVG",
                        direction="BULLISH",
                        confidence=confidence,
                        price_level=(prev_candle.high + next_candle.low) / 2,
                        timestamp=current_candle.timestamp,
                        zone_high=next_candle.low,
                        zone_low=prev_candle.high,
                        description=f"Bullish FVG: {prev_candle.high:.4f} - {next_candle.low:.4f}"
                    ))
            
            # Bearish FVG: Gap between previous low and next high
            elif (prev_candle.low > next_candle.high and 
                  current_candle.close < current_candle.open):
                
                gap_size = prev_candle.low - next_candle.high
                gap_percentage = gap_size / next_candle.high * 100
                
                if gap_percentage > 0.1:
                    confidence = min(90, 50 + gap_percentage * 10)
                    
                    fvgs.append(SMCPattern(
                        pattern_type="FVG",
                        direction="BEARISH",
                        confidence=confidence,
                        price_level=(prev_candle.low + next_candle.high) / 2,
                        timestamp=current_candle.timestamp,
                        zone_high=prev_candle.low,
                        zone_low=next_candle.high,
                        description=f"Bearish FVG: {next_candle.high:.4f} - {prev_candle.low:.4f}"
                    ))
        
        return fvgs
    
    @staticmethod
    def detect_liquidity_sweeps(ohlc_data: List[OHLCData]) -> List[SMCPattern]:
        """Detect liquidity sweeps (stop hunts)"""
        if len(ohlc_data) < 20:
            return []
        
        sweeps = []
        
        # Find significant highs and lows
        for i in range(10, len(ohlc_data) - 5):
            current = ohlc_data[i]
            
            # Check for liquidity above (sweep of highs)
            recent_high = max([c.high for c in ohlc_data[i-10:i]])
            if current.high > recent_high * 1.001:  # Break above by 0.1%
                # Check for quick reversal
                reversal_found = False
                for j in range(i + 1, min(i + 4, len(ohlc_data))):
                    if ohlc_data[j].close < recent_high:
                        reversal_found = True
                        break
                
                if reversal_found:
                    confidence = 75
                    
                    sweeps.append(SMCPattern(
                        pattern_type="LIQUIDITY_SWEEP",
                        direction="BEARISH",
                        confidence=confidence,
                        price_level=current.high,
                        timestamp=current.timestamp,
                        zone_high=current.high,
                        zone_low=recent_high,
                        description=f"Bearish liquidity sweep at {current.high:.4f}, reversal below {recent_high:.4f}"
                    ))
            
            # Check for liquidity below (sweep of lows)
            recent_low = min([c.low for c in ohlc_data[i-10:i]])
            if current.low < recent_low * 0.999:  # Break below by 0.1%
                # Check for quick reversal
                reversal_found = False
                for j in range(i + 1, min(i + 4, len(ohlc_data))):
                    if ohlc_data[j].close > recent_low:
                        reversal_found = True
                        break
                
                if reversal_found:
                    confidence = 75
                    
                    sweeps.append(SMCPattern(
                        pattern_type="LIQUIDITY_SWEEP",
                        direction="BULLISH",
                        confidence=confidence,
                        price_level=current.low,
                        timestamp=current.timestamp,
                        zone_high=recent_low,
                        zone_low=current.low,
                        description=f"Bullish liquidity sweep at {current.low:.4f}, reversal above {recent_low:.4f}"
                    ))
        
        return sweeps