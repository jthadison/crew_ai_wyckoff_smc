from datetime import datetime
from typing import Dict, List
from crewai.tools import BaseTool

from data_structures.ohlc import OHLCData
from data_structures.pattern_results import PatternResult
from tools.pattern_recognition.supporting_classses.candlestick_patterns import CandlestickPatterns
from tools.pattern_recognition.supporting_classses.chart_patterns import ChartPatterns
from tools.pattern_recognition.supporting_classses.harmonic_patterns import HarmonicPatterns
from tools.pattern_recognition.supporting_classses.volume_patterns import VolumePatterns

class PatternRecognitionTool(BaseTool):
    """Main Pattern Recognition Tool for CrewAI integration"""
    
    name: str = "pattern_recognition"
    description: str = "Comprehensive pattern recognition for chart patterns, candlesticks, and trading patterns"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        object.__setattr__(self, '_candlestick_analyzer', CandlestickPatterns())
        object.__setattr__(self, '_chart_analyzer', ChartPatterns())
        object.__setattr__(self, '_harmonic_analyzer', HarmonicPatterns())
        object.__setattr__(self, '_volume_analyzer', VolumePatterns())
    
    @property
    def candlestick_analyzer(self) -> CandlestickPatterns:
        return object.__getattribute__(self, '_candlestick_analyzer') if hasattr(self, '_candlestick_analyzer') else CandlestickPatterns()
    
    @property
    def chart_analyzer(self) -> ChartPatterns:
        return object.__getattribute__(self, '_chart_analyzer') if hasattr(self, '_chart_analyzer') else ChartPatterns()
    
    @property
    def harmonic_analyzer(self) -> HarmonicPatterns:
        return object.__getattribute__(self, '_harmonic_analyzer') if hasattr(self, '_harmonic_analyzer') else HarmonicPatterns()
    
    @property
    def volume_analyzer(self) -> VolumePatterns:
        return object.__getattribute__(self, '_volume_analyzer') if hasattr(self, '_volume_analyzer') else VolumePatterns()
    
    def _run(self, ohlc_data: List[OHLCData], pattern_types: str = "all") -> str:
        """
        Run pattern recognition on OHLC data
        
        Args:
            ohlc_data: List of OHLC data points
            pattern_types: 'all', 'candlestick', 'chart', 'harmonic', 'volume'
        """
        try:
            if not ohlc_data or len(ohlc_data) < 5:
                return "Insufficient data for pattern recognition"
            
            all_patterns = []
            
            # Candlestick patterns
            if pattern_types in ['all', 'candlestick']:
                candlestick_patterns = self.candlestick_analyzer.detect_candlestick_patterns(ohlc_data)
                all_patterns.extend(candlestick_patterns)
            
            # Chart patterns
            if pattern_types in ['all', 'chart']:
                triangle_patterns = self.chart_analyzer.detect_triangle_patterns(ohlc_data)
                hs_patterns = self.chart_analyzer.detect_head_and_shoulders(ohlc_data)
                flag_patterns = self.chart_analyzer.detect_flag_patterns(ohlc_data)
                all_patterns.extend(triangle_patterns + hs_patterns + flag_patterns)
            
            # Harmonic patterns
            if pattern_types in ['all', 'harmonic']:
                gartley_patterns = self.harmonic_analyzer.detect_gartley_pattern(ohlc_data)
                all_patterns.extend(gartley_patterns)
            
            # Volume patterns
            if pattern_types in ['all', 'volume']:
                volume_patterns = self.volume_analyzer.detect_volume_climax(ohlc_data)
                all_patterns.extend(volume_patterns)
            
            # Sort patterns by confidence
            all_patterns.sort(key=lambda p: p.confidence, reverse=True)
            
            return self._format_pattern_output(all_patterns, ohlc_data[0].symbol, ohlc_data[0].timeframe)
            
        except Exception as e:
            return f"Error in pattern recognition: {str(e)}"
    
    def _format_pattern_output(self, patterns: List[PatternResult], symbol: str, timeframe: str) -> str:
        """Format pattern recognition results"""
        output = []
        output.append(f"🔍 PATTERN RECOGNITION - {symbol} ({timeframe})")
        output.append("=" * 60)
        output.append(f"Analysis Time: {datetime.now().isoformat()}")
        output.append(f"Patterns Detected: {len(patterns)}")
        output.append("")
        
        if not patterns:
            output.append("No significant patterns detected.")
            return "\n".join(output)
        
        # Group patterns by type
        pattern_groups = {
            'CANDLESTICK': [],
            'CHART': [],
            'HARMONIC': [],
            'VOLUME': []
        }
        
        for pattern in patterns:
            pattern_groups[pattern.pattern_type].append(pattern)
        
        # Display each group
        for pattern_type, group_patterns in pattern_groups.items():
            if group_patterns:
                output.append(f"📊 {pattern_type} PATTERNS")
                output.append("-" * 30)
                
                for pattern in group_patterns[:3]:  # Top 3 per group
                    output.append(f"• {pattern.pattern_name}")
                    output.append(f"  Direction: {pattern.direction}")
                    output.append(f"  Confidence: {pattern.confidence:.1f}%")
                    output.append(f"  Reliability: {pattern.reliability_score:.1f}%")
                    
                    if pattern.target_price:
                        output.append(f"  Target: {pattern.target_price:.5f}")
                    if pattern.stop_loss:
                        output.append(f"  Stop Loss: {pattern.stop_loss:.5f}")
                    
                    output.append(f"  Description: {pattern.description}")
                    
                    # Key levels
                    if pattern.key_levels:
                        output.append("  Key Levels:")
                        for level_name, level_value in pattern.key_levels.items():
                            if isinstance(level_value, (int, float)):
                                output.append(f"    {level_name}: {level_value:.5f}")
                    
                    output.append("")
        
        # Trading signals based on patterns
        output.append("🎯 PATTERN-BASED SIGNALS")
        output.append("-" * 30)
        
        high_confidence_patterns = [p for p in patterns if p.confidence > 75]
        
        if high_confidence_patterns:
            for pattern in high_confidence_patterns[:3]:
                signal_strength = (pattern.confidence + pattern.reliability_score) / 2
                
                if pattern.direction in ['BULLISH', 'ACCUMULATION']:
                    signal_type = "BUY"
                elif pattern.direction in ['BEARISH', 'DISTRIBUTION']:
                    signal_type = "SELL"
                else:
                    signal_type = "NEUTRAL"
                
                output.append(f"• {signal_type} Signal from {pattern.pattern_name}")
                output.append(f"  Signal Strength: {signal_strength:.1f}%")
                output.append(f"  Reasoning: {pattern.description}")
                output.append("")
        else:
            output.append("No high-confidence signals detected.")
        
        return "\n".join(output)