from datetime import datetime
from typing import Dict, List, Optional
#from .data_structures.confluence_signal import ConfluenceSignal
from data_structures.confluence_signal import ConfluenceSignal
from tools.analyzers.advanced_smc_analyzer import AdvancedSMCAnalyzer
from tools.analyzers.advanced_wyckoff_analyzer import AdvancedWyckoffAnalyzer
from tools.confluence_analyzer import ConfluenceAnalyzer
import numpy as np

class WyckoffSMCTradingSystem:
    """Complete Wyckoff/SMC trading system with confluence analysis"""
    
    def __init__(self):
        self.confluence_analyzer = ConfluenceAnalyzer()
        self.wyckoff_analyzer = AdvancedWyckoffAnalyzer()
        self.smc_analyzer = AdvancedSMCAnalyzer()
    
    def analyze_trading_opportunity(self, ohlc_data: List, technical_indicators: Optional[Dict] = None) -> Dict:
        """Complete trading opportunity analysis"""
        
        # Get confluence signal
        confluence_signal = self.confluence_analyzer.analyze_confluence(
            ohlc_data, technical_indicators if technical_indicators is not None else {}
        )
        
        # Get detailed analysis
        wyckoff_schematic = self.wyckoff_analyzer.detect_wyckoff_schematic(ohlc_data)
        composite_operator = self.wyckoff_analyzer.detect_composite_operator_activity(ohlc_data)
        market_structure = self.smc_analyzer.detect_market_structure_shift(ohlc_data)
        order_flow = self.smc_analyzer.detect_institutional_order_flow(ohlc_data)
        
        return {
            'confluence_signal': confluence_signal,
            'wyckoff_analysis': {
                'schematic': wyckoff_schematic,
                'composite_operator': composite_operator
            },
            'smc_analysis': {
                'market_structure': market_structure,
                'order_flow': order_flow
            },
            'trading_recommendation': self._generate_trading_recommendation(confluence_signal),
            'analysis_timestamp': datetime.now().isoformat()
        }
    
    def _generate_trading_recommendation(self, confluence_signal: ConfluenceSignal) -> Dict:
        """Generate trading recommendation based on confluence"""
        if not confluence_signal or confluence_signal.signal_type == "NEUTRAL":
            return {
                'action': 'WAIT',
                'confidence': 'LOW',
                'reason': 'Insufficient confluence for trade entry'
            }
        
        # Determine confidence level
        if confluence_signal.confluence_score >= 80:
            confidence = 'HIGH'
        elif confluence_signal.confluence_score >= 70:
            confidence = 'MEDIUM'
        else:
            confidence = 'LOW'
        
        # Generate position sizing recommendation (as percentage of account)
        if confidence == 'HIGH':
            position_size = 2.0  # 2% risk
        elif confidence == 'MEDIUM':
            position_size = 1.5  # 1.5% risk
        else:
            position_size = 1.0  # 1% risk
        
        return {
            'action': confluence_signal.signal_type,
            'confidence': confidence,
            'position_size_percent': position_size,
            'entry_price': confluence_signal.entry_price,
            'stop_loss': confluence_signal.stop_loss,
            'take_profit': confluence_signal.take_profit,
            'risk_reward_ratio': confluence_signal.risk_reward_ratio,
            'confluence_score': confluence_signal.confluence_score,
            'reasoning': confluence_signal.reasoning
        }

# Test function
def test_wyckoff_smc_analyzer():
    """Test the Wyckoff/SMC analyzer"""
    print("🧪 TESTING WYCKOFF/SMC ANALYZER")
    print("=" * 50)
    
    # Create sample data with some patterns
    sample_data = []
    base_price = 1.2000
    
    # Create accumulation pattern
    for i in range(150):
        if i < 50:  # Initial decline (selling climax)
            price_change = np.random.normal(-0.001, 0.0005)
            volume_multiplier = 2.0 if i > 40 else 1.0
        elif i < 100:  # Consolidation phase
            price_change = np.random.normal(0, 0.0002)
            volume_multiplier = 0.5
        else:  # Spring and markup
            price_change = np.random.normal(0.0005, 0.0003)
            volume_multiplier = 1.5
        
        new_price = base_price * (1 + price_change)
        high = new_price * (1 + abs(np.random.normal(0, 0.0002)))
        low = new_price * (1 - abs(np.random.normal(0, 0.0002)))
        volume = abs(np.random.normal(1000, 200)) * volume_multiplier
        
        sample_data.append(type('OHLCData', (), {
            'symbol': "EURUSD",
            'timeframe': "1H", 
            'timestamp': datetime.now(),
            'open': base_price,
            'high': high,
            'low': low,
            'close': new_price,
            'volume': volume
        })())
        
        base_price = new_price
    
    # Test the complete system
    try:
        print("Testing WyckoffSMCTradingSystem...")
        trading_system = WyckoffSMCTradingSystem()
        
        # Add some mock technical indicators
        tech_indicators = {
            'rsi': {'value': 25.5},  # Oversold
            'macd': {'histogram': 0.001}  # Bullish
        }
        
        analysis = trading_system.analyze_trading_opportunity(sample_data, tech_indicators)
        
        print("✅ Analysis completed successfully!")
        print(f"Signal: {analysis['confluence_signal'].signal_type if analysis['confluence_signal'] else 'NONE'}")
        print(f"Confluence Score: {analysis['confluence_signal'].confluence_score:.1f}% if analysis['confluence_signal'] else 'N/A'")
        print(f"Recommendation: {analysis['trading_recommendation']['action']}")
        print(f"Confidence: {analysis['trading_recommendation']['confidence']}")
        
        # Test confluence summary
        if analysis['confluence_signal']:
            confluence_analyzer = ConfluenceAnalyzer()
            summary = confluence_analyzer.get_confluence_summary(analysis['confluence_signal'])
            print("\n" + "="*50)
            print("CONFLUENCE SUMMARY:")
            print("="*50)
            print(summary[:500] + "..." if len(summary) > 500 else summary)
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n🎉 Wyckoff/SMC Analyzer testing complete!")

if __name__ == "__main__":
    test_wyckoff_smc_analyzer()