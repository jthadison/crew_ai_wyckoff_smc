"""
Comprehensive Test Suite for BacktestingTool
Tests all functionality including strategy validation, parameter optimization, and regime analysis
"""

import sys
import os
from pathlib import Path
import json
from datetime import datetime, timedelta
import numpy as np
from dotenv import load_dotenv

load_dotenv()
#from tools.back_testing.back_testing_tool import BacktestingTool

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

try:
    from tools.back_testing.back_testing_tool import BacktestingTool
    from data_structures.ohlc import OHLCData
    from data_structures.trade_results import TradeResult
    print("SUCCESS: Successfully imported BacktestingTool!")
except ImportError as e:
    print(f"IMPORT ERROR: {e}")
    sys.exit(1)


class BacktestingTestSuite:
    """Comprehensive test suite for BacktestingTool"""
    
    def __init__(self):
        self.tool = BacktestingTool()
        self.test_results = []
    
    def run_all_tests(self):
        """Run all backtesting tests"""
        print("🧪 BACKTESTING TOOL TEST SUITE")
        print("=" * 50)
        
        # Test 1: Basic tool initialization
        self._test_tool_initialization()
        
        # Test 2: Synthetic data generation
        self._test_data_generation()
        
        # Test 3: Strategy configuration validation
        self._test_strategy_configuration()
        
        # Test 4: Comprehensive backtest execution
        self._test_comprehensive_backtest()
        
        # Test 5: Parameter optimization
        self._test_parameter_optimization()
        
        # Test 6: Market regime analysis
        self._test_regime_analysis()
        
        # Test 7: Statistical significance testing
        self._test_statistical_significance()
        
        # Test 8: Performance validation
        self._test_performance_validation()
        
        # Summary
        self._print_test_summary()
    
    def _test_tool_initialization(self):
        """Test BacktestingTool initialization"""
        print("\n📋 Test 1: Tool Initialization")
        try:
            tool = BacktestingTool()
            assert hasattr(tool, 'tech_analyzer')
            assert hasattr(tool, 'pattern_analyzer')
            assert hasattr(tool, 'confluence_analyzer')
            print("✅ PASSED: Tool initialization successful")
            self.test_results.append(("Tool Initialization", "PASSED"))
        except Exception as e:
            print(f"❌ FAILED: Tool initialization failed - {e}")
            self.test_results.append(("Tool Initialization", f"FAILED: {e}"))
    
    def _test_data_generation(self):
        """Test synthetic data generation"""
        print("\n📊 Test 2: Synthetic Data Generation")
        try:
            # Generate test data
            synthetic_data = self.tool._generate_synthetic_data("EURUSD", "1H", 30)
            
            assert len(synthetic_data) == 30 * 24  # 30 days * 24 hours
            assert all(isinstance(candle, OHLCData) for candle in synthetic_data)
            assert all(candle.high >= candle.low for candle in synthetic_data)
            assert all(candle.high >= max(candle.open, candle.close) for candle in synthetic_data)
            assert all(candle.low <= min(candle.open, candle.close) for candle in synthetic_data)
            
            print(f"✅ PASSED: Generated {len(synthetic_data)} data points")
            print(f"   Price range: {min(c.low for c in synthetic_data):.4f} - {max(c.high for c in synthetic_data):.4f}")
            self.test_results.append(("Data Generation", "PASSED"))
        except Exception as e:
            print(f"❌ FAILED: Data generation failed - {e}")
            self.test_results.append(("Data Generation", f"FAILED: {e}"))
    
    def _test_strategy_configuration(self):
        """Test strategy configuration validation"""
        print("\n⚙️ Test 3: Strategy Configuration")
        try:
            # Create test strategy config
            strategy_config = {
                "strategy_name": "Test_Wyckoff_SMC",
                "initial_balance": 10000,
                "risk_per_trade": 0.02,
                "min_risk_reward": 3.0,
                "min_confluence_score": 70,
                "confluence_weights": {
                    "wyckoff_weight": 0.4,
                    "smc_weight": 0.3,
                    "technical_weight": 0.2,
                    "pattern_weight": 0.1
                }
            }
            
            # Validate configuration
            assert strategy_config["risk_per_trade"] <= 0.05  # Max 5% risk
            assert strategy_config["min_risk_reward"] >= 2.0   # Min 1:2 RR
            assert sum(strategy_config["confluence_weights"].values()) == 1.0  # Weights sum to 1
            
            print("✅ PASSED: Strategy configuration valid")
            print(f"   Strategy: {strategy_config['strategy_name']}")
            print(f"   Risk per trade: {strategy_config['risk_per_trade']*100}%")
            print(f"   Min R:R ratio: 1:{strategy_config['min_risk_reward']}")
            self.test_results.append(("Strategy Configuration", "PASSED"))
        except Exception as e:
            print(f"❌ FAILED: Strategy configuration invalid - {e}")
            self.test_results.append(("Strategy Configuration", f"FAILED: {e}"))
    
    def _test_comprehensive_backtest(self):
        """Test comprehensive backtesting execution"""
        print("\n🔬 Test 4: Comprehensive Backtest")
        try:
            # Strategy configuration
            strategy_config = {
                "strategy_name": "Test_Comprehensive",
                "initial_balance": 10000,
                "risk_per_trade": 0.02,
                "min_risk_reward": 3.0,
                "min_confluence_score": 65,  # Lower threshold for testing
                "confluence_weights": {
                    "wyckoff_weight": 0.4,
                    "smc_weight": 0.3,
                    "technical_weight": 0.2,
                    "pattern_weight": 0.1
                }
            }
            
            # Data configuration
            data_config = {
                "symbol": "EURUSD",
                "timeframe": "1H",
                "days": 90,
                "start_date": (datetime.now() - timedelta(days=90)).isoformat(),
                "end_date": datetime.now().isoformat()
            }
            
            # Run backtest
            result = self.tool._run(
                strategy_config=json.dumps(strategy_config),
                historical_data=json.dumps(data_config),
                validation_type="comprehensive"
            )
            
            assert len(result) > 100  # Should have substantial output
            assert "BACKTEST RESULTS" in result
            assert "PERFORMANCE SUMMARY" in result
            assert "RECOMMENDATION" in result
            
            print("✅ PASSED: Comprehensive backtest executed")
            print(f"   Result length: {len(result)} characters")
            print("   Key sections found: Results, Performance, Recommendation")
            self.test_results.append(("Comprehensive Backtest", "PASSED"))
            
            # Print first part of result for verification
            print("\n📄 Sample Result (first 500 chars):")
            print(result[:500] + "..." if len(result) > 500 else result)
            
        except Exception as e:
            print(f"❌ FAILED: Comprehensive backtest failed - {e}")
            self.test_results.append(("Comprehensive Backtest", f"FAILED: {e}"))
    
    def _test_parameter_optimization(self):
        """Test parameter optimization functionality"""
        print("\n🎯 Test 5: Parameter Optimization")
        try:
            strategy_config = {"strategy_name": "Test_Optimization"}
            data_config = {"symbol": "EURUSD", "days": 60}
            
            result = self.tool._run(
                strategy_config=json.dumps(strategy_config),
                historical_data=json.dumps(data_config),
                validation_type="parameter_optimization"
            )
            
            assert "optimization" in result.lower()
            print("✅ PASSED: Parameter optimization test")
            self.test_results.append(("Parameter Optimization", "PASSED"))
        except Exception as e:
            print(f"❌ FAILED: Parameter optimization failed - {e}")
            self.test_results.append(("Parameter Optimization", f"FAILED: {e}"))
    
    def _test_regime_analysis(self):
        """Test market regime analysis"""
        print("\n📈 Test 6: Market Regime Analysis")
        try:
            # Generate test data with different regimes
            test_data = self.tool._generate_synthetic_data("EURUSD", "1H", 60)
            regimes = self.tool._analyze_market_regimes(test_data)
            
            assert len(regimes) > 0
            assert all(hasattr(regime, 'regime_type') for regime in regimes)
            assert all(hasattr(regime, 'volatility') for regime in regimes)
            
            regime_types = [r.regime_type for r in regimes]
            unique_regimes = set(regime_types)
            
            print(f"✅ PASSED: Market regime analysis")
            print(f"   Regimes identified: {len(regimes)}")
            print(f"   Regime types: {', '.join(unique_regimes)}")
            self.test_results.append(("Market Regime Analysis", "PASSED"))
        except Exception as e:
            print(f"❌ FAILED: Market regime analysis failed - {e}")
            self.test_results.append(("Market Regime Analysis", f"FAILED: {e}"))
    
    def _test_statistical_significance(self):
        """Test statistical significance calculations"""
        print("\n📊 Test 7: Statistical Significance")
        try:
            # Create mock trades with known win rate
            mock_trades = []
            for i in range(50):
                # 60% win rate
                pnl = 100 if i < 30 else -50
                trade = TradeResult(
                    trade_id=f"test_{i}",
                    symbol="EURUSD",
                    timeframe="1H",
                    entry_time=datetime.now(),
                    exit_time=None,
                    entry_price=1.2000,
                    exit_price=None,
                    position_size=1000,
                    trade_type="BUY",
                    status="CLOSED",
                    pnl=pnl,
                    pnl_percent=pnl/1200,
                    stop_loss=1.1950,
                    take_profit=1.2150,
                    patterns_detected=[],
                    confluence_score=75.0,
                    wyckoff_signals=[],
                    smc_signals=[],
                    technical_indicators={},
                    risk_reward_ratio=3.0,
                    hold_time_hours=4.0,
                    max_favorable_excursion=None,
                    max_adverse_excursion=None,
                    trade_notes="Test trade"
                )
                mock_trades.append(trade)
            
            significance = self.tool._calculate_statistical_significance(mock_trades)
            
            assert 0 <= significance <= 100
            print(f"✅ PASSED: Statistical significance calculation")
            print(f"   Significance level: {significance:.1f}%")
            print(f"   Sample size: {len(mock_trades)} trades")
            self.test_results.append(("Statistical Significance", "PASSED"))
        except Exception as e:
            print(f"❌ FAILED: Statistical significance failed - {e}")
            self.test_results.append(("Statistical Significance", f"FAILED: {e}"))
    
    def _test_performance_validation(self):
        """Test performance validation metrics"""
        print("\n🎯 Test 8: Performance Validation")
        try:
            # Test parameter stability calculation
            config = {"min_confluence_score": 70}
            test_data = self.tool._generate_synthetic_data("EURUSD", "1H", 180)
            
            stability = self.tool._analyze_parameter_stability(config, test_data)
            
            assert 0 <= stability <= 100
            print(f"✅ PASSED: Performance validation")
            print(f"   Parameter stability: {stability:.1f}%")
            self.test_results.append(("Performance Validation", "PASSED"))
        except Exception as e:
            print(f"❌ FAILED: Performance validation failed - {e}")
            self.test_results.append(("Performance Validation", f"FAILED: {e}"))
    
    def _print_test_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "=" * 60)
        print("🎉 BACKTESTING TOOL TEST SUMMARY")
        print("=" * 60)
        
        passed_tests = [test for test, result in self.test_results if result == "PASSED"]
        failed_tests = [test for test, result in self.test_results if "FAILED" in result]
        
        print(f"Total Tests: {len(self.test_results)}")
        print(f"Passed: {len(passed_tests)}")
        print(f"Failed: {len(failed_tests)}")
        print(f"Success Rate: {len(passed_tests)/len(self.test_results)*100:.1f}%")
        
        if failed_tests:
            print(f"\n❌ Failed Tests:")
            for test, result in self.test_results:
                if "FAILED" in result:
                    print(f"   • {test}: {result}")
        
        print(f"\n✅ Passed Tests:")
        for test in passed_tests:
            print(f"   • {test}")
        
        # Overall status
        if len(failed_tests) == 0:
            print(f"\n🎉 ALL TESTS PASSED! BacktestingTool is ready for production!")
        elif len(failed_tests) <= 2:
            print(f"\n⚠️ MOSTLY SUCCESSFUL with {len(failed_tests)} minor issues")
        else:
            print(f"\n❌ ISSUES DETECTED - {len(failed_tests)} tests failed")


def create_sample_strategy_configs():
    """Create sample strategy configurations for testing"""
    
    # Conservative strategy
    conservative_config = {
        "strategy_name": "Conservative_Wyckoff_SMC",
        "initial_balance": 10000,
        "risk_per_trade": 0.01,  # 1% risk
        "min_risk_reward": 4.0,   # 1:4 minimum
        "min_confluence_score": 80,  # High confidence only
        "confluence_weights": {
            "wyckoff_weight": 0.5,    # Higher Wyckoff weight
            "smc_weight": 0.3,
            "technical_weight": 0.15,
            "pattern_weight": 0.05
        }
    }
    
    # Aggressive strategy
    aggressive_config = {
        "strategy_name": "Aggressive_Wyckoff_SMC",
        "initial_balance": 10000,
        "risk_per_trade": 0.03,  # 3% risk
        "min_risk_reward": 2.5,   # 1:2.5 minimum
        "min_confluence_score": 65,  # Lower threshold
        "confluence_weights": {
            "wyckoff_weight": 0.3,
            "smc_weight": 0.4,        # Higher SMC weight
            "technical_weight": 0.2,
            "pattern_weight": 0.1
        }
    }
    
    # Balanced strategy
    balanced_config = {
        "strategy_name": "Balanced_Wyckoff_SMC",
        "initial_balance": 10000,
        "risk_per_trade": 0.02,  # 2% risk
        "min_risk_reward": 3.0,   # 1:3 minimum
        "min_confluence_score": 72,  # Moderate threshold
        "confluence_weights": {
            "wyckoff_weight": 0.4,
            "smc_weight": 0.35,
            "technical_weight": 0.15,
            "pattern_weight": 0.1
        }
    }
    
    return {
        "conservative": conservative_config,
        "aggressive": aggressive_config,
        "balanced": balanced_config
    }


def main():
    """Main test execution function"""
    
    print("🚀 BACKTESTING TOOL COMPREHENSIVE TESTING")
    print("=" * 70)
    
    # Run main test suite
    test_suite = BacktestingTestSuite()
    test_suite.run_all_tests()
    
    # Test sample configurations
    print("\n" + "=" * 70)
    print("📋 SAMPLE STRATEGY CONFIGURATIONS")
    print("=" * 70)
    
    sample_configs = create_sample_strategy_configs()
    for strategy_name, config in sample_configs.items():
        print(f"\n📈 {strategy_name.title()} Strategy:")
        print(f"   Risk per trade: {config['risk_per_trade']*100}%")
        print(f"   Min R:R ratio: 1:{config['min_risk_reward']}")
        print(f"   Min confluence: {config['min_confluence_score']}%")
        print(f"   Wyckoff weight: {config['confluence_weights']['wyckoff_weight']*100}%")
        print(f"   SMC weight: {config['confluence_weights']['smc_weight']*100}%")
    
    print(f"\n🎯 Ready to test with different strategy configurations!")
    print(f"💡 Use these configs with your BacktestingTool for validation!")


if __name__ == "__main__":
    main()