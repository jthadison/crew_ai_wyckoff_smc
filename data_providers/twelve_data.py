from datetime import datetime
import os
from typing import List, Optional

import requests
from data_structures.ohlc import OHLCData
from .utilities.safe_date_conversion import SafeDateConversion


class TwelveDataProvider:
    """Twelve Data API provider"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('TWELVE_DATA_API_KEY')
        self.base_url = "https://api.twelvedata.com"
        
    def get_ohlc_data(self, symbol: str, timeframe: str, count: int = 100) -> List[OHLCData]:
        """Fetch OHLC data from Twelve Data"""
        
        if not self.api_key:
            raise ValueError("Twelve Data API key not found. Set TWELVE_DATA_API_KEY environment variable.")
        
        # Map our timeframes to Twelve Data format
        timeframe_map = {
            '1M': '1min',
            '5M': '5min',
            '15M': '15min',
            '1H': '1h',
            '4H': '4h',
            '1D': '1day'
        }
        
        td_timeframe = timeframe_map.get(timeframe, '1h')
        
        params = {
            'symbol': symbol,
            'interval': td_timeframe,
            'outputsize': count,
            'apikey': self.api_key
        }
        
        try:
            response = requests.get(f"{self.base_url}/time_series", params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'values' not in data:
                raise ValueError(f"No data returned for {symbol}")
            
            ohlc_data = []
            for item in data['values']:
                try:
                    # Safe datetime conversion
                    dt = SafeDateConversion.safe_datetime_conversion(item['datetime'])
                    if dt is None:
                        # Try alternative datetime parsing for Twelve Data format
                        try:
                            dt = datetime.strptime(item['datetime'], '%Y-%m-%d %H:%M:%S')
                        except ValueError:
                            try:
                                dt = datetime.strptime(item['datetime'], '%Y-%m-%d')
                            except ValueError:
                                print(f"Warning: Could not parse datetime {item['datetime']}")
                                continue
                    
                    ohlc_data.append(OHLCData(
                        symbol=symbol,
                        timeframe=timeframe,
                        timestamp=dt,
                        open=SafeDateConversion.safe_float_conversion(item['open']),
                        high=SafeDateConversion.safe_float_conversion(item['high']),
                        low=SafeDateConversion.safe_float_conversion(item['low']),
                        close=SafeDateConversion.safe_float_conversion(item['close']),
                        volume=SafeDateConversion.safe_float_conversion(item['volume'])
                    ))
                except Exception as e:
                    print(f"Warning: Could not process Twelve Data item: {e}")
                    continue
            
            return sorted(ohlc_data, key=lambda x: x.timestamp)
            
        except Exception as e:
            print(f"Error fetching data from Twelve Data: {e}")
            return []