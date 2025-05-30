from dataclasses import dataclass

from pydantic import Field
import os
from typing import List
from data_providers import twelve_data, yahoo_financial, trading_view
from tools.market_analyzer_tool import MarketAnalyzer
from data_providers.twelve_data import TwelveDataProvider
from data_providers.yahoo_financial import YahooFinanceProvider
from data_structures.ohlc import OHLCData
#from test import MarketAnalyzer
from crewai.tools import BaseTool
from tools.market_analyzer_tool import MarketAnalyzer

@dataclass
class MarketDataTool(BaseTool):
    name: str = Field(default="market_data_fetcher", description="Tool name")
    description: str = Field(default="Fetches real-time market data and performs market structure analysis", description="Tool description")
    
    # Use model_config instead of class Config for Pydantic v2
    model_config = {"arbitrary_types_allowed": True}
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Use object.__setattr__ to bypass Pydantic's attribute protection
        object.__setattr__(self, '_yahoo_finance', YahooFinanceProvider())
        object.__setattr__(self, '_twelve_data', TwelveDataProvider())
        object.__setattr__(self, '_analyzer', MarketAnalyzer())
        object.__setattr__(self, '_primary_provider', "yahoo" if not os.getenv('TWELVE_DATA_API_KEY') else "twelve_data")
    
    @property
    def yahoo_finance(self):
        """Access Yahoo Finance provider"""
        return getattr(self, '_yahoo_finance', YahooFinanceProvider())
    
    @property
    def twelve_data(self):
        """Access Twelve Data provider"""
        return getattr(self, '_twelve_data', TwelveDataProvider())
    
    @property
    def analyzer(self):
        """Access Market Analyzer"""
        return getattr(self, '_analyzer', MarketAnalyzer())
    
    @property
    def primary_provider(self):
        """Access primary provider setting"""
        return getattr(self, '_primary_provider', "yahoo")
    
    def _run(self, symbol: str, timeframe: str = "1H", analysis_type: str = "structure", count: int = 100) -> str:
        """
        Fetch market data and perform analysis
        
        Args:
            symbol: Trading symbol (US30, NAS100, SP500, EURUSD, etc.)
            timeframe: Time frame (1M, 5M, 15M, 1H, 4H, 1D)
            analysis_type: Type of analysis (structure, ohlc, swing_points)
            count: Number of candles to fetch
        """
        
        try:
            # Fetch OHLC data
            ohlc_data = self._fetch_ohlc_data(symbol, timeframe, count)
            
            if not ohlc_data:
                return f"No data available for {symbol} on {timeframe}"
            
            # Perform requested analysis
            if analysis_type == "ohlc":
                return self._format_ohlc_data(ohlc_data)
            elif analysis_type == "structure":
                return self._analyze_market_structure(symbol, ohlc_data)
            elif analysis_type == "swing_points":
                return self._analyze_swing_points(ohlc_data)
            else:
                return self._analyze_market_structure(symbol, ohlc_data)
                
        except Exception as e:
            return f"Error fetching market data: {str(e)}"
    
    def _fetch_ohlc_data(self, symbol: str, timeframe: str, count: int) -> List[OHLCData]:
        """Fetch OHLC data from the best available provider"""
        
        providers = [
            ("twelve_data", TwelveDataProvider),
            ("yahoo", YahooFinanceProvider()),
            # ("tradingview", self.tradingview)  # Disabled for now
        ]
        
        # Try primary provider first
        if self.primary_provider != "twelve_data":
            providers = [("yahoo", yahoo_financial), ("twelve_data", twelve_data)]
        
        for provider_name, provider in providers:
            try:
                print(f"Trying {provider_name} for {symbol} {timeframe}")
                data = provider.get_ohlc_data(symbol, timeframe, count)
                if data:
                    print(f"Successfully fetched {len(data)} candles from {provider_name}")
                    return data
            except Exception as e:
                print(f"Provider {provider_name} failed: {e}")
                continue
        
        return []
    
    def _format_ohlc_data(self, data: List[OHLCData]) -> str:
        """Format OHLC data for output"""
        
        if not data:
            return "No OHLC data available"
        
        recent_data = data[-10:]  # Last 10 candles
        
        output = f"OHLC Data ({len(data)} candles):\n"
        output += "Timestamp | Open | High | Low | Close | Volume\n"
        output += "-" * 60 + "\n"
        
        for candle in recent_data:
            output += f"{candle.timestamp.strftime('%Y-%m-%d %H:%M')} | "
            output += f"{candle.open:.4f} | {candle.high:.4f} | "
            output += f"{candle.low:.4f} | {candle.close:.4f} | {candle.volume:.0f}\n"
        
        return output
    
    def _analyze_market_structure(self, symbol: str, data: List[OHLCData]) -> str:
        """Perform comprehensive market structure analysis"""
        #analyzer = MarketAnalyzer()
        # Get swing points
        swing_points = self.analyzer.identify_swing_points(data)
        
        # Get support/resistance levels
        levels = self.analyzer.identify_support_resistance(data, swing_points)
        
        # Determine market bias
        bias = self.analyzer.determine_market_bias(data)
        
        # Format output
        current_price = data[-1].close
        output = f"Market Structure Analysis for {symbol}:\n"
        output += "=" * 50 + "\n"
        output += f"Current Price: {current_price:.4f}\n"
        output += f"Market Bias: {bias.upper()}\n"
        output += f"Data Points: {len(data)} candles\n\n"
        
        # Swing highs
        output += "Recent Swing Highs:\n"
        for high in swing_points['swing_highs'][-5:]:
            output += f"  {high['timestamp'][:16]} - {high['price']:.4f}\n"
        
        output += "\nRecent Swing Lows:\n"
        for low in swing_points['swing_lows'][-5:]:
            output += f"  {low['timestamp'][:16]} - {low['price']:.4f}\n"
        
        # Support/Resistance
        output += f"\nKey Resistance Levels:\n"
        for level in levels['resistance_levels']:
            distance = ((level - current_price) / current_price) * 100
            output += f"  {level:.4f} ({distance:+.2f}%)\n"
        
        output += f"\nKey Support Levels:\n"
        for level in levels['support_levels']:
            distance = ((level - current_price) / current_price) * 100
            output += f"  {level:.4f} ({distance:+.2f}%)\n"
        
        # Trend analysis
        output += f"\nTrend Analysis:\n"
        if len(data) >= 20:
            recent_highs = [point['price'] for point in swing_points['swing_highs'][-3:]]
            recent_lows = [point['price'] for point in swing_points['swing_lows'][-3:]]
            
            if len(recent_highs) >= 2:
                hh_trend = "Higher Highs" if recent_highs[-1] > recent_highs[-2] else "Lower Highs"
                output += f"  {hh_trend}\n"
            
            if len(recent_lows) >= 2:
                ll_trend = "Higher Lows" if recent_lows[-1] > recent_lows[-2] else "Lower Lows"
                output += f"  {ll_trend}\n"
        
        return output
    
    def _analyze_swing_points(self, data: List[OHLCData]) -> str:
        """Analyze swing points specifically"""
        
        swing_points = self.analyzer.identify_swing_points(data)
        
        output = "Swing Point Analysis:\n"
        output += "=" * 30 + "\n"
        
        output += f"Swing Highs Found: {len(swing_points['swing_highs'])}\n"
        output += f"Swing Lows Found: {len(swing_points['swing_lows'])}\n\n"
        
        # Recent swing highs
        output += "Last 5 Swing Highs:\n"
        for high in swing_points['swing_highs'][-5:]:
            output += f"  {high['timestamp'][:16]} - {high['price']:.4f}\n"
        
        output += "\nLast 5 Swing Lows:\n"
        for low in swing_points['swing_lows'][-5:]:
            output += f"  {low['timestamp'][:16]} - {low['price']:.4f}\n"
        
        return output
