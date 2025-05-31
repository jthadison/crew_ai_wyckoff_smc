"""
Test Runner Script
Runs tests with proper path configuration
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

def run_tests():
    """Run all tests"""
    print("TESTING: Running Trading System Tests")
    print("=" * 50)
    
    try:
        # Import and run the test suite
        from tests.performance_analytics_test_suite import PerformanceAnalyticsTestSuite
        
        test_suite = PerformanceAnalyticsTestSuite()
        test_suite.run_all_tests()
        
    except ImportError as e:
        print(f"ERROR: Could not import test suite: {e}")
        print("\nTrying to run basic import tests...")
        
        # Basic import test
        try:
            from data_structures.ohlc import OHLCData
            print("SUCCESS: OHLCData import successful")
        except ImportError as e:
            print(f"FAILED: OHLCData import failed: {e}")
        
        try:
            from data_structures.trade_results import TradeResult
            print("SUCCESS: TradeResult import successful")
        except ImportError as e:
            print(f"FAILED: TradeResult import failed: {e}")

if __name__ == "__main__":
    run_tests()
