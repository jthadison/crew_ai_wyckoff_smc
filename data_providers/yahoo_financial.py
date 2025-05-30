from typing import List

import yfinance as yf
from data_structures.ohlc import OHLCData
from .utilities.safe_date_conversion import SafeDateConversion


class YahooFinanceProvider:
    """Yahoo Finance provider using yfinance"""
    
    def __init__(self):
        pass
    
    def get_ohlc_data(self, symbol: str, timeframe: str, count: int = 100) -> List[OHLCData]:
        """Fetch OHLC data from Yahoo Finance"""
        
        # Map our symbols to Yahoo Finance format
        symbol_map = {
            'US30': '^DJI',      # Dow Jones
            'NAS100': '^NDX',    # Nasdaq 100
            'SP500': '^GSPC',    # S&P 500
            'EURUSD': 'EURUSD=X',
            'GBPUSD': 'GBPUSD=X',
            'USDJPY': 'USDJPY=X',
            'USDCHF': 'USDCHF=X',
            'AUDUSD': 'AUDUSD=X',
            'USDCAD': 'USDCAD=X'
        }
        
        # Map timeframes
        timeframe_map = {
            '1M': '1m',
            '5M': '5m',
            '15M': '15m',
            '1H': '1h',
            '4H': '4h',
            '1D': '1d'
        }
        
        yf_symbol = symbol_map.get(symbol, symbol)
        yf_timeframe = timeframe_map.get(timeframe, '1h')
        
        try:
            # Calculate period based on timeframe and count
            if timeframe in ['1M', '5M']:
                period = '7d'  # Last 7 days for minute data
            elif timeframe in ['15M', '1H']:
                period = '60d'  # Last 60 days for hourly data
            else:
                period = '1y'   # Last year for daily data
            
            ticker = yf.Ticker(yf_symbol)
            df = ticker.history(period=period, interval=yf_timeframe)
            
            if df.empty:
                raise ValueError(f"No data returned for {symbol}")
            
            # Take last 'count' rows
            df = df.tail(count)
            
            ohlc_data = []
            for timestamp, row in df.iterrows():
                # Safe datetime conversion
                dt = SafeDateConversion.safe_datetime_conversion(timestamp)
                if dt is None:
                    continue
                
                # Safe float conversions with validation
                open_price = SafeDateConversion.safe_float_conversion(row['Open'])
                high_price = SafeDateConversion.safe_float_conversion(row['High'])
                low_price = SafeDateConversion.safe_float_conversion(row['Low'])
                close_price = SafeDateConversion.safe_float_conversion(row['Close'])
                volume = SafeDateConversion.safe_float_conversion(row['Volume'])
                
                # Skip rows with invalid data
                if all(price == 0.0 for price in [open_price, high_price, low_price, close_price]):
                    print(f"Warning: Skipping row with all zero prices for {timestamp}")
                    continue
                
                try:
                    ohlc_data.append(OHLCData(
                        symbol=symbol,
                        timeframe=timeframe,
                        timestamp=dt,
                        open=open_price,
                        high=high_price,
                        low=low_price,
                        close=close_price,
                        volume=volume
                    ))
                except Exception as e:
                    print(f"Warning: Could not create OHLCData for {timestamp}: {e}")
                    continue
            
            return ohlc_data
            
        except Exception as e:
            print(f"Error fetching data from Yahoo Finance: {e}")
            return []