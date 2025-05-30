from datetime import datetime
from typing import Dict, List
from crewai.tools import BaseTool

from data_structures.ohlc import OHLCData
from tools.analyzers.smc_analyzer import SMCAnalyzer
from tools.technical_analysis.supporting_classes.technical_indicator import TechnicalIndicators
#from tools.wyckoff_analysis_tool import WyckoffAnalyzer

import numpy as np

from tools.technical_analysis.supporting_classes.wyckoff_analysis_tool import WyckoffAnalyzer

class TechnicalAnalysisTool(BaseTool):
    """Main Technical Analysis Tool for CrewAI integration"""
    
    name: str = "technical_analysis"
    description: str = "Comprehensive technical analysis with Wyckoff and SMC pattern recognition"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        object.__setattr__(self, 'indicators', TechnicalIndicators())
        object.__setattr__(self, 'wyckoff_analyzer', WyckoffAnalyzer())
        object.__setattr__(self, 'smc_analyzer', SMCAnalyzer())
    
    @property
    def indicators(self) -> TechnicalIndicators:
        return object.__getattribute__(self, '_indicators') if hasattr(self, '_indicators') else TechnicalIndicators()
    
    @property
    def wyckoff_analyzer(self) -> WyckoffAnalyzer:
        return object.__getattribute__(self, '_wyckoff_analyzer') if hasattr(self, '_wyckoff_analyzer') else WyckoffAnalyzer()
    
    @property
    def smc_analyzer(self) -> SMCAnalyzer:
        return object.__getattribute__(self, '_smc_analyzer') if hasattr(self, '_smc_analyzer') else SMCAnalyzer()
    
    def _run(self, ohlc_data: List[OHLCData], analysis_type: str = "comprehensive") -> str:
        """
        Run technical analysis on OHLC data
        
        Args:
            ohlc_data: List of OHLC data points
            analysis_type: 'indicators', 'wyckoff', 'smc', or 'comprehensive'
        """
        try:
            if not ohlc_data or len(ohlc_data) < 10:
                return "Insufficient data for technical analysis"
            
            results = {
                'symbol': ohlc_data[0].symbol,
                'timeframe': ohlc_data[0].timeframe,
                'analysis_time': datetime.now().isoformat(),
                'data_points': len(ohlc_data)
            }
            
            closes = [candle.close for candle in ohlc_data]
            highs = [candle.high for candle in ohlc_data]
            lows = [candle.low for candle in ohlc_data]
            
            if analysis_type in ['indicators', 'comprehensive']:
                # Calculate technical indicators
                rsi_values = self.indicators.rsi(closes)
                macd_data = self.indicators.macd(closes)
                bb_data = self.indicators.bollinger_bands(closes)
                stoch_data = self.indicators.stochastic(highs, lows, closes)
                
                current_rsi = rsi_values[-1] if not np.isnan(rsi_values[-1]) else None
                current_macd = macd_data['macd'][-1] if not np.isnan(macd_data['macd'][-1]) else None
                
                results['indicators'] = {
                    'rsi': {
                        'value': current_rsi,
                        'signal': 'OVERSOLD' if current_rsi and current_rsi < 30 else 'OVERBOUGHT' if current_rsi and current_rsi > 70 else 'NEUTRAL'
                    },
                    'macd': {
                        'macd': current_macd,
                        'signal': macd_data['signal'][-1] if not np.isnan(macd_data['signal'][-1]) else None,
                        'histogram': macd_data['histogram'][-1] if not np.isnan(macd_data['histogram'][-1]) else None
                    },
                    'bollinger_bands': {
                        'upper': bb_data['upper'][-1] if not np.isnan(bb_data['upper'][-1]) else None,
                        'middle': bb_data['middle'][-1] if not np.isnan(bb_data['middle'][-1]) else None,
                        'lower': bb_data['lower'][-1] if not np.isnan(bb_data['lower'][-1]) else None,
                        'position': 'ABOVE_UPPER' if closes[-1] > bb_data['upper'][-1] else 'BELOW_LOWER' if closes[-1] < bb_data['lower'][-1] else 'WITHIN_BANDS'
                    }
                }
            
            if analysis_type in ['wyckoff', 'comprehensive']:
                # Wyckoff analysis
                accumulation = self.wyckoff_analyzer.detect_accumulation_phase(ohlc_data)
                distribution = self.wyckoff_analyzer.detect_distribution_phase(ohlc_data)
                spring = self.wyckoff_analyzer.detect_spring(ohlc_data)
                
                wyckoff_patterns = []
                if accumulation:
                    wyckoff_patterns.append({
                        'type': accumulation.pattern_type,
                        'phase': accumulation.phase,
                        'confidence': accumulation.confidence,
                        'description': accumulation.description,
                        'key_levels': accumulation.key_levels
                    })
                
                if distribution:
                    wyckoff_patterns.append({
                        'type': distribution.pattern_type,
                        'phase': distribution.phase,
                        'confidence': distribution.confidence,
                        'description': distribution.description,
                        'key_levels': distribution.key_levels
                    })
                
                if spring:
                    wyckoff_patterns.append({
                        'type': spring.pattern_type,
                        'phase': spring.phase,
                        'confidence': spring.confidence,
                        'description': spring.description,
                        'key_levels': spring.key_levels
                    })
                
                results['wyckoff'] = {
                    'patterns_detected': len(wyckoff_patterns),
                    'patterns': wyckoff_patterns
                }
            
            if analysis_type in ['smc', 'comprehensive']:
                # SMC analysis
                order_blocks = self.smc_analyzer.detect_order_blocks(ohlc_data)
                fvgs = self.smc_analyzer.detect_fair_value_gaps(ohlc_data)
                liquidity_sweeps = self.smc_analyzer.detect_liquidity_sweeps(ohlc_data)
                
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
                
                for sweep in liquidity_sweeps:
                    smc_patterns.append({
                        'type': sweep.pattern_type,
                        'direction': sweep.direction,
                        'confidence': sweep.confidence,
                        'price_level': sweep.price_level,
                        'description': sweep.description
                    })
                
                results['smc'] = {
                    'order_blocks': len([p for p in smc_patterns if p['type'] == 'ORDER_BLOCK']),
                    'fair_value_gaps': len([p for p in smc_patterns if p['type'] == 'FVG']),
                    'liquidity_sweeps': len([p for p in smc_patterns if p['type'] == 'LIQUIDITY_SWEEP']),
                    'patterns': smc_patterns
                }
            
            # Generate trading signals based on analysis
            signals = self._generate_signals(results, ohlc_data)
            results['signals'] = signals
            
            # Format output
            return self._format_analysis_output(results)
            
        except Exception as e:
            return f"Error in technical analysis: {str(e)}"
    
    def _generate_signals(self, analysis_results: Dict, ohlc_data: List[OHLCData]) -> List[Dict]:
        """Generate trading signals based on technical analysis"""
        signals = []
        current_price = ohlc_data[-1].close
        
        # RSI signals
        if 'indicators' in analysis_results and analysis_results['indicators']['rsi']['value']:
            rsi_value = analysis_results['indicators']['rsi']['value']
            if rsi_value < 30:
                signals.append({
                    'type': 'BUY',
                    'source': 'RSI',
                    'strength': 70,
                    'price': current_price,
                    'reason': f'RSI oversold at {rsi_value:.1f}'
                })
            elif rsi_value > 70:
                signals.append({
                    'type': 'SELL',
                    'source': 'RSI',
                    'strength': 70,
                    'price': current_price,
                    'reason': f'RSI overbought at {rsi_value:.1f}'
                })
        
        # Wyckoff signals
        if 'wyckoff' in analysis_results:
            for pattern in analysis_results['wyckoff']['patterns']:
                if pattern['type'] == 'SPRING' and pattern['confidence'] > 70:
                    signals.append({
                        'type': 'BUY',
                        'source': 'WYCKOFF_SPRING',
                        'strength': pattern['confidence'],
                        'price': pattern['key_levels'].get('entry_level', current_price),
                        'reason': f"Wyckoff spring detected: {pattern['description']}"
                    })
                elif pattern['type'] == 'ACCUMULATION' and pattern['confidence'] > 75:
                    signals.append({
                        'type': 'BUY',
                        'source': 'WYCKOFF_ACCUMULATION',
                        'strength': pattern['confidence'] * 0.8,  # Slightly lower strength
                        'price': current_price,
                        'reason': f"Accumulation phase: {pattern['description']}"
                    })
                elif pattern['type'] == 'DISTRIBUTION' and pattern['confidence'] > 75:
                    signals.append({
                        'type': 'SELL',
                        'source': 'WYCKOFF_DISTRIBUTION',
                        'strength': pattern['confidence'] * 0.8,
                        'price': current_price,
                        'reason': f"Distribution phase: {pattern['description']}"
                    })
        
        # SMC signals
        if 'smc' in analysis_results:
            for pattern in analysis_results['smc']['patterns']:
                if pattern['confidence'] > 70:
                    if pattern['type'] == 'ORDER_BLOCK':
                        if pattern['direction'] == 'BULLISH':
                            signals.append({
                                'type': 'BUY',
                                'source': 'SMC_ORDER_BLOCK',
                                'strength': pattern['confidence'],
                                'price': pattern['zone_low'],
                                'reason': f"Bullish order block: {pattern['description']}"
                            })
                        else:
                            signals.append({
                                'type': 'SELL',
                                'source': 'SMC_ORDER_BLOCK',
                                'strength': pattern['confidence'],
                                'price': pattern['zone_high'],
                                'reason': f"Bearish order block: {pattern['description']}"
                            })
                    
                    elif pattern['type'] == 'FVG':
                        if pattern['direction'] == 'BULLISH':
                            signals.append({
                                'type': 'BUY',
                                'source': 'SMC_FVG',
                                'strength': pattern['confidence'] * 0.9,
                                'price': pattern['zone_low'],
                                'reason': f"Bullish FVG: {pattern['description']}"
                            })
                        else:
                            signals.append({
                                'type': 'SELL',
                                'source': 'SMC_FVG',
                                'strength': pattern['confidence'] * 0.9,
                                'price': pattern['zone_high'],
                                'reason': f"Bearish FVG: {pattern['description']}"
                            })
                    
                    elif pattern['type'] == 'LIQUIDITY_SWEEP':
                        signals.append({
                            'type': 'BUY' if pattern['direction'] == 'BULLISH' else 'SELL',
                            'source': 'SMC_LIQUIDITY_SWEEP',
                            'strength': pattern['confidence'],
                            'price': current_price,
                            'reason': pattern['description']
                        })
        
        # Sort signals by strength
        signals.sort(key=lambda x: x['strength'], reverse=True)
        
        return signals
    
    def _format_analysis_output(self, results: Dict) -> str:
        """Format analysis results for output"""
        output = []
        output.append(f"📊 TECHNICAL ANALYSIS - {results['symbol']} ({results['timeframe']})")
        output.append("=" * 60)
        output.append(f"Analysis Time: {results['analysis_time']}")
        output.append(f"Data Points: {results['data_points']}")
        output.append("")
        
        # Technical Indicators
        if 'indicators' in results:
            output.append("📈 TECHNICAL INDICATORS")
            output.append("-" * 30)
            
            rsi_data = results['indicators']['rsi']
            if rsi_data['value']:
                output.append(f"RSI (14): {rsi_data['value']:.2f} - {rsi_data['signal']}")
            
            macd_data = results['indicators']['macd']
            if macd_data['macd']:
                output.append(f"MACD: {macd_data['macd']:.4f}")
                output.append(f"Signal: {macd_data['signal']:.4f}")
                output.append(f"Histogram: {macd_data['histogram']:.4f}")
            
            bb_data = results['indicators']['bollinger_bands']
            if bb_data['upper']:
                output.append(f"Bollinger Bands:")
                output.append(f"  Upper: {bb_data['upper']:.4f}")
                output.append(f"  Middle: {bb_data['middle']:.4f}")
                output.append(f"  Lower: {bb_data['lower']:.4f}")
                output.append(f"  Position: {bb_data['position']}")
            
            output.append("")
        
        # Wyckoff Analysis
        if 'wyckoff' in results:
            output.append("🏛️ WYCKOFF ANALYSIS")
            output.append("-" * 30)
            output.append(f"Patterns Detected: {results['wyckoff']['patterns_detected']}")
            
            for pattern in results['wyckoff']['patterns']:
                output.append(f"• {pattern['type']} - {pattern['phase']}")
                output.append(f"  Confidence: {pattern['confidence']:.1f}%")
                output.append(f"  Description: {pattern['description']}")
                
                if 'key_levels' in pattern:
                    output.append("  Key Levels:")
                    for level_name, level_value in pattern['key_levels'].items():
                        if isinstance(level_value, (int, float)):
                            output.append(f"    {level_name}: {level_value:.4f}")
                output.append("")
        
        # SMC Analysis
        if 'smc' in results:
            output.append("💰 SMART MONEY CONCEPTS")
            output.append("-" * 30)
            output.append(f"Order Blocks: {results['smc']['order_blocks']}")
            output.append(f"Fair Value Gaps: {results['smc']['fair_value_gaps']}")
            output.append(f"Liquidity Sweeps: {results['smc']['liquidity_sweeps']}")
            output.append("")
            
            # Show top patterns by confidence
            top_patterns = sorted(results['smc']['patterns'], 
                                key=lambda x: x['confidence'], reverse=True)[:5]
            
            if top_patterns:
                output.append("Top SMC Patterns:")
                for pattern in top_patterns:
                    output.append(f"• {pattern['type']} ({pattern['direction']})")
                    output.append(f"  Confidence: {pattern['confidence']:.1f}%")
                    output.append(f"  Price Level: {pattern['price_level']:.4f}")
                    output.append(f"  Description: {pattern['description']}")
                    output.append("")
        
        # Trading Signals
        if 'signals' in results:
            output.append("🎯 TRADING SIGNALS")
            output.append("-" * 30)
            
            if not results['signals']:
                output.append("No significant trading signals detected.")
            else:
                output.append(f"Total Signals: {len(results['signals'])}")
                output.append("")
                
                # Group signals by type
                buy_signals = [s for s in results['signals'] if s['type'] == 'BUY']
                sell_signals = [s for s in results['signals'] if s['type'] == 'SELL']
                
                if buy_signals:
                    output.append("🟢 BUY SIGNALS:")
                    for signal in buy_signals[:3]:  # Top 3
                        output.append(f"• {signal['source']} (Strength: {signal['strength']:.1f}%)")
                        output.append(f"  Price: {signal['price']:.4f}")
                        output.append(f"  Reason: {signal['reason']}")
                        output.append("")
                
                if sell_signals:
                    output.append("🔴 SELL SIGNALS:")
                    for signal in sell_signals[:3]:  # Top 3
                        output.append(f"• {signal['source']} (Strength: {signal['strength']:.1f}%)")
                        output.append(f"  Price: {signal['price']:.4f}")
                        output.append(f"  Reason: {signal['reason']}")
                        output.append("")
        
        return "\n".join(output)