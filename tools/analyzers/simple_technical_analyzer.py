from typing import Dict, List
from data_structures.ohlc import OHLCData
from tools.analyzers.smc_analyzer import SMCAnalyzer
from tools.technical_analysis.technical_analysis_tool import TechnicalAnalysisTool
from tools.technical_analysis.supporting_classes.technical_indicator import TechnicalIndicators
#from tools.technical_analysis.supporting_classes.wyckoff_analysis_tool import WyckoffAnalyzer
from analyzers.wyckoff_analyzer import WyckoffAnalyzer


class SimpleTechnicalAnalyzer:
    """Simplified technical analyzer that doesn't inherit from BaseTool"""
    
    def __init__(self):
        self.indicators = TechnicalIndicators()
        self.wyckoff_analyzer = WyckoffAnalyzer()
        self.smc_analyzer = SMCAnalyzer()
    
    def analyze(self, ohlc_data: List[OHLCData], analysis_type: str = "comprehensive") -> str:
        """Run technical analysis - same as TechnicalAnalysisTool._run"""
        tool = TechnicalAnalysisTool()
        return tool._run(ohlc_data, analysis_type)
    
    def get_signals_only(self, ohlc_data: List[OHLCData]) -> List[Dict]:
        """Get just the trading signals without full analysis"""
        if not ohlc_data or len(ohlc_data) < 10:
            return []
        
        # Run minimal analysis to get patterns
        results = {}
        
        # Quick Wyckoff check
        spring = self.wyckoff_analyzer.detect_spring(ohlc_data)
        accumulation = self.wyckoff_analyzer.detect_accumulation_phase(ohlc_data)
        
        wyckoff_patterns = []
        if spring:
            wyckoff_patterns.append({
                'type': spring.pattern_type,
                'confidence': spring.confidence,
                'key_levels': spring.key_levels,
                'description': spring.description
            })
        if accumulation:
            wyckoff_patterns.append({
                'type': accumulation.pattern_type,
                'confidence': accumulation.confidence,
                'key_levels': accumulation.key_levels,
                'description': accumulation.description
            })
        
        results['wyckoff'] = {'patterns': wyckoff_patterns}
        
        # Quick SMC check
        order_blocks = self.smc_analyzer.detect_order_blocks(ohlc_data)
        fvgs = self.smc_analyzer.detect_fair_value_gaps(ohlc_data)
        
        smc_patterns = []
        for ob in order_blocks:
            smc_patterns.append({
                'type': ob.pattern_type,
                'direction': ob.direction,
                'confidence': ob.confidence,
                'price_level': ob.price_level,
                'zone_high': ob.zone_high,
                'zone_low': ob.zone_low,
                'description': ob.description
            })
        
        for fvg in fvgs:
            smc_patterns.append({
                'type': fvg.pattern_type,
                'direction': fvg.direction,
                'confidence': fvg.confidence,
                'price_level': fvg.price_level,
                'zone_high': fvg.zone_high,
                'zone_low': fvg.zone_low,
                'description': fvg.description
            })
        
        results['smc'] = {'patterns': smc_patterns}
        
        # Generate signals
        tool = TechnicalAnalysisTool()
        return tool._generate_signals(results, ohlc_data)