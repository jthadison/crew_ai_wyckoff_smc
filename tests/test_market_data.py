"""
Market Data Tool Implementation
Supporting Twelve Data, Yahoo Finance, and TradingView integration
"""

import os
from pathlib import Path
import sys
import requests
import pandas as pd
# custom_tools import MarketDataTool

# SOLUTION: Add project root to Python path
current_dir = Path(__file__).parent  # tests folder
project_root = current_dir.parent    # project root folder

# Add project root to path
print(f"Current directory: {current_dir}")
print(f"Project root: {project_root}")

# Add project root to Python path
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
    print(f"Added project root to Python path: {str(project_root)}")
    
from tools.market_data_tool import MarketDataTool
from data_providers.trading_view import TradingViewProvider
from data_providers.twelve_data import TwelveDataProvider
from data_providers.yahoo_financial import YahooFinanceProvider
from data_structures.ohlc import OHLCData
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
import json
import time
from dataclasses import dataclass
from crewai.tools import BaseTool
from dotenv import load_dotenv

load_dotenv()


def test_market_data_tool():
    """Test the market data tool"""
    
    tool = MarketDataTool()
    
    # Test different symbols and timeframes
    test_cases = [
        ("US30", "1H", "structure"),
        ("EURUSD", "15M", "ohlc"),
        ("NAS100", "4H", "swing_points")
    ]
    
    for symbol, timeframe, analysis in test_cases:
        print(f"\n{'='*60}")
        print(f"Testing {symbol} - {timeframe} - {analysis}")
        print('='*60)
        
        result = tool._run(symbol, timeframe, analysis)
        print(result)
        
        time.sleep(1)  # Rate limiting

if __name__ == "__main__":
    # Set up your API keys
    # os.environ['TWELVE_DATA_API_KEY'] = 'your-api-key-here'
    
    test_market_data_tool()