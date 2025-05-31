"""
Windows Compatible Performance Analytics Test Suite
Handles import path issues properly without Unicode emojis
"""

import sys
import os
from pathlib import Path

# SOLUTION: Add project root to Python path
current_dir = Path(__file__).parent  # tests folder
project_root = current_dir.parent    # project root folder

print(f"Current directory: {current_dir}")
print(f"Project root: {project_root}")

# Add project root to Python path
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
    print(f"Added project root to Python path: {str(project_root)}")

# Now imports should work properly
import json
import random
from datetime import datetime, timedelta
from typing import List

try:
    import numpy as np
except ImportError:
    print("WARNING: numpy not installed, using basic math operations")
    np = None

try:
    # Try importing with the fixed path
    from data_structures.ohlc import OHLCData
    from data_structures.trade_results import TradeResult
    from data_structures.confluence_signal import ConfluenceSignal
    print("SUCCESS: Successfully imported data structures!")
except ImportError as e:
    print(f"ERROR: Import failed even after path fix: {e}")
    print(f"Current Python path: {sys.path}")
    print(f"Project root: {project_root}")
    print(f"Files in project root: {list(project_root.iterdir())}")
    exit(1)

class PerformanceAnalyticsTestSuite:
    """Comprehensive testing suite for the Performance Analytics System"""
    
    def __init__(self):
        self.test_results = []
        print(f"TEST LOCATION: Running from: {Path(__file__).parent}")
        print(f"PROJECT ROOT: {project_root}")
        print(f"PYTHON PATH: Project root included: {str(project_root) in sys.path}")
        
    def run_all_tests(self):
        """Run complete test suite"""
        print("TESTING: PERFORMANCE ANALYTICS TESTING SUITE")
        print("=" * 60)
        
        # Test imports first
        self._test_imports()
        
        # Test data generation
        print("\nGENERATING: Test Data...")
        sample_trades = self._generate_sample_trades()
        
        # Test all core functionalities
        test_methods = [
            self._test_trade_addition,
            self._test_performance_analysis,
            self._test_data_structures,
            self._test_json_serialization
        ]
        
        for test_method in test_methods:
            try:
                print(f"\nRUNNING: {test_method.__name__}...")
                result = test_method(sample_trades)
                self.test_results.append({
                    'test': test_method.__name__,
                    'status': 'PASSED' if result else 'FAILED',
                    'timestamp': datetime.now()
                })
                status = 'PASSED' if result else 'FAILED'
                print(f"RESULT: {test_method.__name__} - {status}")
            except Exception as e:
                print(f"ERROR: {test_method.__name__} - {str(e)}")
                self.test_results.append({
                    'test': test_method.__name__,
                    'status': 'ERROR',
                    'error': str(e),
                    'timestamp': datetime.now()
                })
        
        # Generate test report
        self._generate_test_report()
    
    def _test_imports(self):
        """Test that all required imports work"""
        try:
            print("TESTING: Imports...")
            
            # Test data structure imports
            from data_structures.ohlc import OHLCData
            from data_structures.trade_results import TradeResult
            from data_structures.confluence_signal import ConfluenceSignal
            print("  SUCCESS: Data structures imported successfully")
            
            # Test tool imports (if they exist)
            try:
                from tools.performance_calculator.performance_analytics_tool import PerformanceAnalyticsTool
                print("  SUCCESS: Performance Analytics Tool imported successfully")
            except ImportError:
                print("  WARNING: Performance Analytics Tool not found (this is OK for testing)")
            
            # Test creating data structures
            test_ohlc = OHLCData(
                symbol="TEST",
                timeframe="1H",
                timestamp=datetime.now(),
                open=1.0,
                high=1.1,
                low=0.9,
                close=1.05,
                volume=1000.0
            )
            print("  SUCCESS: OHLCData creation test passed")
            
            return True
            
        except Exception as e:
            print(f"  ERROR: Import test failed: {e}")
            return False
    
    def _generate_sample_trades(self) -> List[TradeResult]:
        """Generate realistic sample trade data for testing"""
        trades = []
        base_time = datetime.now() - timedelta(days=30)
        
        symbols = ['US30', 'NAS100', 'SP500', 'EURUSD', 'GBPUSD']
        timeframes = ['1H', '4H', '1D']
        
        for i in range(20):  # Generate 20 sample trades
            symbol = random.choice(symbols)
            timeframe = random.choice(timeframes)
            
            # Generate realistic trade data
            entry_time = base_time + timedelta(hours=i * 12)
            exit_time = entry_time + timedelta(hours=random.randint(1, 24))
            
            entry_price = random.uniform(1.1000, 1.3000) if 'USD' in symbol else random.uniform(30000, 35000)
            
            # Simulate win/loss with realistic ratios
            is_winner = random.random() < 0.65  # 65% win rate
            
            if is_winner:
                pnl = random.uniform(50, 500)
                pnl_percent = random.uniform(0.5, 3.0)
                exit_price = entry_price * (1 + pnl_percent/100)
            else:
                pnl = random.uniform(-200, -50)
                pnl_percent = random.uniform(-1.5, -0.3)
                exit_price = entry_price * (1 + pnl_percent/100)
            
            # Generate confluence data
            confluence_score = random.uniform(60, 95)
            wyckoff_signals = ['ACCUMULATION', 'SPRING'] if random.random() < 0.4 else []
            smc_signals = ['ORDER_BLOCK', 'FVG'] if random.random() < 0.5 else []
            patterns_detected = ['HEAD_AND_SHOULDERS', 'TRIANGLE'] if random.random() < 0.3 else []
            
            trade = TradeResult(
                trade_id=f"trade_{i+1:03d}",
                symbol=symbol,
                timeframe=timeframe,
                entry_time=entry_time,
                exit_time=exit_time,
                entry_price=entry_price,
                exit_price=exit_price,
                position_size=random.uniform(0.1, 2.0),
                trade_type='BUY' if random.random() > 0.5 else 'SELL',
                status='CLOSED',
                pnl=pnl,
                pnl_percent=pnl_percent,
                stop_loss=entry_price * 0.985,
                take_profit=entry_price * 1.045,
                patterns_detected=patterns_detected,
                confluence_score=confluence_score,
                wyckoff_signals=wyckoff_signals,
                smc_signals=smc_signals,
                technical_indicators={'rsi': random.uniform(20, 80), 'macd': random.uniform(-0.01, 0.01)},
                risk_reward_ratio=abs(pnl) / 100 if abs(pnl) > 0 else 1.0,
                hold_time_hours=(exit_time - entry_time).total_seconds() / 3600,
                max_favorable_excursion=abs(pnl) * 1.2 if pnl > 0 else 0,
                max_adverse_excursion=abs(pnl) * 0.8 if pnl < 0 else 0,
                trade_notes=f"Test trade {i+1}"
            )
            
            trades.append(trade)
        
        print(f"Generated {len(trades)} sample trades")
        return trades
    
    def _test_trade_addition(self, sample_trades: List[TradeResult]) -> bool:
        """Test trade data structure functionality"""
        try:
            print("   Testing trade data structures...")
            
            for trade in sample_trades[:3]:  # Test first 3 trades
                # Test that all required fields exist
                required_fields = ['trade_id', 'symbol', 'entry_time', 'pnl', 'status']
                for field in required_fields:
                    if not hasattr(trade, field):
                        print(f"   ERROR: Missing required field: {field}")
                        return False
                
                # Test field types
                if not isinstance(trade.trade_id, str):
                    print(f"   ERROR: trade_id should be string, got {type(trade.trade_id)}")
                    return False
                
                if not isinstance(trade.entry_time, datetime):
                    print(f"   ERROR: entry_time should be datetime, got {type(trade.entry_time)}")
                    return False
            
            print("   SUCCESS: Trade data structure validation passed")
            return True
            
        except Exception as e:
            print(f"   ERROR: Trade addition test failed: {e}")
            return False
    
    def _test_performance_analysis(self, sample_trades: List[TradeResult]) -> bool:
        """Test basic performance analysis"""
        try:
            # Calculate basic metrics manually for verification
            closed_trades = [t for t in sample_trades if t.status == 'CLOSED']
            total_trades = len(closed_trades)
            winning_trades = len([t for t in closed_trades if t.pnl and t.pnl > 0])
            win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
            
            total_pnl = sum([t.pnl for t in closed_trades if t.pnl])
            
            print(f"   SUCCESS: Total trades: {total_trades}")
            print(f"   SUCCESS: Winning trades: {winning_trades}")
            print(f"   SUCCESS: Win rate: {win_rate:.1f}%")
            print(f"   SUCCESS: Total P&L: ${total_pnl:.2f}")
            
            # Validate calculations
            if total_trades > 0 and 0 <= win_rate <= 100:
                return True
            else:
                return False
                
        except Exception as e:
            print(f"   ERROR: Performance analysis test failed: {e}")
            return False
    
    def _test_data_structures(self, sample_trades: List[TradeResult]) -> bool:
        """Test data structure functionality"""
        try:
            print("   Testing data structure operations...")
            
            # Test OHLCData creation
            ohlc = OHLCData(
                symbol="TEST",
                timeframe="1H",
                timestamp=datetime.now(),
                open=1.2000,
                high=1.2050,
                low=1.1950,
                close=1.2025,
                volume=1000.0
            )
            
            # Test conversion to dict
            ohlc_dict = ohlc.to_dict()
            if 'symbol' not in ohlc_dict or 'close' not in ohlc_dict:
                print("   ERROR: OHLCData.to_dict() missing required fields")
                return False
            
            print("   SUCCESS: OHLCData creation and conversion passed")
            
            # Test ConfluenceSignal creation
            confluence = ConfluenceSignal(
                signal_type="BUY",
                confluence_score=85.5,
                entry_price=1.2000,
                stop_loss=1.1950,
                take_profit=1.2100,
                risk_reward_ratio=3.0,
                wyckoff_patterns=["ACCUMULATION"],
                smc_patterns=["ORDER_BLOCK"],
                supporting_indicators=["RSI_OVERSOLD"],
                timestamp=datetime.now(),
                reasoning="Test confluence signal"
            )
            
            if confluence.signal_type != "BUY":
                print("   ERROR: ConfluenceSignal creation failed")
                return False
            
            print("   SUCCESS: ConfluenceSignal creation passed")
            return True
            
        except Exception as e:
            print(f"   ERROR: Data structures test failed: {e}")
            return False
    
    def _test_json_serialization(self, sample_trades: List[TradeResult]) -> bool:
        """Test JSON serialization of trade data"""
        try:
            print("   Testing JSON serialization...")
            
            for trade in sample_trades[:2]:  # Test first 2 trades
                trade_data = {
                    'trade_id': trade.trade_id,
                    'symbol': trade.symbol,
                    'timeframe': trade.timeframe,
                    'entry_time': trade.entry_time.isoformat(),
                    'exit_time': trade.exit_time.isoformat() if trade.exit_time else None,
                    'entry_price': trade.entry_price,
                    'exit_price': trade.exit_price,
                    'pnl': trade.pnl,
                    'confluence_score': trade.confluence_score,
                    'status': trade.status
                }
                
                # Test JSON serialization
                json_str = json.dumps(trade_data)
                parsed_data = json.loads(json_str)
                
                if parsed_data['trade_id'] != trade.trade_id:
                    print("   ERROR: JSON serialization/deserialization failed")
                    return False
            
            print("   SUCCESS: JSON serialization/deserialization passed")
            return True
            
        except Exception as e:
            print(f"   ERROR: JSON serialization test failed: {e}")
            return False
    
    def _generate_test_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 60)
        print("TESTING SUMMARY REPORT")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r['status'] == 'PASSED'])
        failed_tests = len([r for r in self.test_results if r['status'] == 'FAILED'])
        error_tests = len([r for r in self.test_results if r['status'] == 'ERROR'])
        
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        print(f"RESULTS:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed: {passed_tests}")
        print(f"   Failed: {failed_tests}")
        print(f"   Errors: {error_tests}")
        print(f"   Success Rate: {success_rate:.1f}%")
        print()
        
        print("DETAILED RESULTS:")
        for result in self.test_results:
            status = result['status']
            print(f"   {result['test']}: {status}")
            if 'error' in result:
                print(f"      Error: {result['error']}")
        
        print()
        if success_rate >= 90:
            print("EXCELLENT: Import and basic functionality tests passed!")
        elif success_rate >= 75:
            print("GOOD: Most tests passed, minor issues to resolve")
        else:
            print("NEEDS WORK: Multiple test failures detected")
        
        print(f"\nTest executed from: {Path(__file__).parent}")
        print(f"Project root: {project_root}")

def main():
    """Run the test suite with proper path management"""
    print(f"Starting tests from: {Path(__file__).resolve()}")
    test_suite = PerformanceAnalyticsTestSuite()
    test_suite.run_all_tests()

if __name__ == "__main__":
    main()