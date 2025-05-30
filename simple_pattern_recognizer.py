# Standalone version for direct usage
from datetime import datetime, timedelta
from typing import Dict, List
from data_structures.ohlc import OHLCData
from data_structures.pattern_results import PatternResult
from tools.pattern_recognition.pattern_recognition_tool import PatternRecognitionTool
from tools.pattern_recognition.supporting_classses.candlestick_patterns import CandlestickPatterns
from tools.pattern_recognition.supporting_classses.chart_patterns import ChartPatterns
from tools.pattern_recognition.supporting_classses.harmonic_patterns import HarmonicPatterns
from tools.pattern_recognition.supporting_classses.volume_patterns import VolumePatterns
import numpy as np


class SimplePatternRecognizer:
    """Simplified pattern recognizer that doesn't inherit from BaseTool"""
    
    def __init__(self):
        self.candlestick_analyzer = CandlestickPatterns()
        self.chart_analyzer = ChartPatterns()
        self.harmonic_analyzer = HarmonicPatterns()
        self.volume_analyzer = VolumePatterns()
    
    def recognize_patterns(self, ohlc_data: List[OHLCData], pattern_types: str = "all") -> List[PatternResult]:
        """Get pattern results without formatting"""
        all_patterns = []
        
        if pattern_types in ['all', 'candlestick']:
            all_patterns.extend(self.candlestick_analyzer.detect_candlestick_patterns(ohlc_data))
        
        if pattern_types in ['all', 'chart']:
            all_patterns.extend(self.chart_analyzer.detect_triangle_patterns(ohlc_data))
            all_patterns.extend(self.chart_analyzer.detect_head_and_shoulders(ohlc_data))
            all_patterns.extend(self.chart_analyzer.detect_flag_patterns(ohlc_data))
        
        if pattern_types in ['all', 'harmonic']:
            all_patterns.extend(self.harmonic_analyzer.detect_gartley_pattern(ohlc_data))
        
        if pattern_types in ['all', 'volume']:
            all_patterns.extend(self.volume_analyzer.detect_volume_climax(ohlc_data))
        
        all_patterns.sort(key=lambda p: p.confidence, reverse=True)
        return all_patterns
    
    def get_trading_signals(self, patterns: List[PatternResult]) -> List[Dict]:
        """Convert patterns to trading signals"""
        signals = []
        
        for pattern in patterns:
            if pattern.confidence > 70:
                if pattern.direction in ['BULLISH', 'ACCUMULATION']:
                    signal_type = "BUY"
                elif pattern.direction in ['BEARISH', 'DISTRIBUTION']:
                    signal_type = "SELL"
                else:
                    continue  # Skip neutral patterns
                
                signal_strength = (pattern.confidence + pattern.reliability_score) / 2
                
                signals.append({
                    'type': signal_type,
                    'source': f"PATTERN_{pattern.pattern_type}",
                    'pattern_name': pattern.pattern_name,
                    'strength': signal_strength,
                    'price': pattern.target_price,
                    'stop_loss': pattern.stop_loss,
                    'reason': pattern.description,
                    'formation_time': pattern.formation_time.total_seconds() / 3600  # hours
                })
        
        return signals

# Test function
def test_pattern_recognition():
    """Test the pattern recognition tool"""
    print("🧪 TESTING PATTERN RECOGNITION TOOL")
    print("=" * 50)
    
    # Create sample data with various patterns
    sample_data = []
    base_price = 1.2000
    
    # Create data with potential patterns
    for i in range(50):
        if i < 10:  # Downtrend for H&S left shoulder
            price_change = np.random.normal(-0.002, 0.001)
        elif i < 20:  # Rally for H&S head
            price_change = np.random.normal(0.003, 0.001)
        elif i < 30:  # Decline for H&S right shoulder
            price_change = np.random.normal(-0.002, 0.001)
        elif i < 40:  # Flag pattern setup
            price_change = np.random.normal(0.004, 0.0005)  # Strong move up
        else:  # Consolidation
            price_change = np.random.normal(0, 0.0002)
        
        new_price = base_price * (1 + price_change)
        high = new_price * (1 + abs(np.random.normal(0, 0.0005)))
        low = new_price * (1 - abs(np.random.normal(0, 0.0005)))
        volume = abs(np.random.normal(1000, 300))
        
        # Create some special candles
        if i == 15:  # Doji
            new_price = base_price
        elif i == 25:  # Hammer
            low = new_price * 0.995
            new_price = new_price * 0.998
        
        sample_data.append(OHLCData(
            symbol="EURUSD",
            timeframe="1H",
            timestamp=datetime.now() + timedelta(hours=i),
            open=base_price,
            high=high,
            low=low,
            close=new_price,
            volume=volume
        ))
        
        base_price = new_price
    
    # Test SimplePatternRecognizer
    try:
        print("Testing SimplePatternRecognizer...")
        recognizer = SimplePatternRecognizer()
        patterns = recognizer.recognize_patterns(sample_data, "all")
        
        print(f"✅ Found {len(patterns)} patterns")
        for pattern in patterns[:5]:  # Top 5
            print(f"  • {pattern.pattern_name} ({pattern.pattern_type}) - {pattern.confidence:.1f}%")
        
        signals = recognizer.get_trading_signals(patterns)
        print(f"✅ Generated {len(signals)} trading signals")
        
    except Exception as e:
        print(f"❌ SimplePatternRecognizer failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Test PatternRecognitionTool (CrewAI version)
    try:
        print("\nTesting PatternRecognitionTool (CrewAI version)...")
        tool = PatternRecognitionTool()
        result = tool._run(sample_data, "all")
        print("✅ PatternRecognitionTool works!")
        print("\nSample output (first 800 chars):")
        print(result[:800] + "..." if len(result) > 800 else result)
        
    except Exception as e:
        print(f"❌ PatternRecognitionTool failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n🎉 Pattern Recognition Tool testing complete!")

if __name__ == "__main__":
    test_pattern_recognition()