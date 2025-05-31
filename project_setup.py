#!/usr/bin/env python3
"""
Project Setup Script
Creates necessary __init__.py files and sets up proper Python package structure
"""

import os
from pathlib import Path

def create_init_files():
    """Create __init__.py files for proper package structure"""
    
    project_root = Path(__file__).parent
    print(f"Setting up project structure in: {project_root}")
    
    # Directories that need __init__.py files
    package_dirs = [
        'data_structures',
        'tools',
        'tools/analyzers',
        'tools/performance_calculator',
        'tools/performance_calculator/supporting_class',
        'tools/pattern_recognition',
        'tools/pattern_recognition/supporting_classses',
        'tools/technical_analysis',
        'tools/technical_analysis/supporting_classes',
        'tools/back_testing',
        'tools/back_testing/supporting_classes',
        'data_providers',
        'data_providers/utilities',
        'tests'
    ]
    
    # Content for different __init__.py files
    init_contents = {
        'data_structures': '''"""
Data structures package for the Wyckoff/SMC trading system
"""

try:
    from .ohlc import OHLCData
    from .trade_results import TradeResult
    from .confluence_signal import ConfluenceSignal
    from .wyckoff_pattern import WyckoffPattern
    from .smc_pattern import SMCPattern
    from .performance_metrics import PerformanceMetrics
    from .pattern_results import PatternResult
    from .pattern_performance import PatternPerformance
    
    __all__ = [
        'OHLCData',
        'TradeResult', 
        'ConfluenceSignal',
        'WyckoffPattern',
        'SMCPattern',
        'PerformanceMetrics',
        'PatternResult',
        'PatternPerformance'
    ]
except ImportError as e:
    # Some modules might not exist yet
    print(f"Warning: Could not import all data structures: {e}")
    __all__ = []
''',
        
        'tools': '''"""
Tools package for the trading system
"""

try:
    from .market_data_tool import MarketDataTool
    from .technical_analysis.technical_analysis_tool import TechnicalAnalysisTool
    from .pattern_recognition.pattern_recognition_tool import PatternRecognitionTool
    from .performance_calculator.performance_analytics_tool import PerformanceAnalyticsTool
    
    __all__ = [
        'MarketDataTool',
        'TechnicalAnalysisTool',
        'PatternRecognitionTool',
        'PerformanceAnalyticsTool'
    ]
except ImportError as e:
    print(f"Warning: Could not import all tools: {e}")
    __all__ = []
''',
        
        'tests': '''"""
Tests package
"""
''',
        
        'default': '''"""
Package module
"""
'''
    }
    
    created_files = []
    
    for package_dir in package_dirs:
        dir_path = project_root / package_dir
        
        # Create directory if it doesn't exist
        if not dir_path.exists():
            print(f"Creating directory: {dir_path}")
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Create __init__.py file
        init_file = dir_path / '__init__.py'
        
        if not init_file.exists():
            # Choose appropriate content
            content = init_contents.get(package_dir.split('/')[0], init_contents['default'])
            
            with open(init_file, 'w') as f:
                f.write(content)
            
            created_files.append(str(init_file))
            print(f"CREATED: {init_file}")
        else:
            print(f"EXISTS: {init_file}")
    
    return created_files

def check_project_structure():
    """Check if the project has the expected structure"""
    
    project_root = Path(__file__).parent
    expected_files = [
        'data_structures/ohlc.py',
        'data_structures/trade_results.py',
        'data_structures/confluence_signal.py',
        'tools/market_data_tool.py',
        'main.py'
    ]
    
    print("\nCHECKING: Checking project structure...")
    
    for file_path in expected_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"FOUND: {file_path}")
        else:
            print(f"MISSING: {file_path}")
    
    # Check for Python files in data_structures
    data_structures_dir = project_root / 'data_structures'
    if data_structures_dir.exists():
        py_files = list(data_structures_dir.glob('*.py'))
        print(f"\nDATA STRUCTURES: Directory contains {len(py_files)} Python files:")
        for py_file in py_files:
            if py_file.name != '__init__.py':
                print(f"   FILE: {py_file.name}")

def create_test_runner():
    """Create a test runner script"""
    
    project_root = Path(__file__).parent
    test_runner = project_root / 'run_tests.py'
    
    runner_content = '''python3
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
        print("\\nTrying to run basic import tests...")
        
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
'''
    
    with open(test_runner, 'w', encoding='utf-8') as f:
        f.write(runner_content)
    
    # Make it executable on Unix systems
    if os.name != 'nt':  # Not Windows
        os.chmod(test_runner, 0o755)
    
    print(f"CREATED: Test runner: {test_runner}")

def main():
    """Main setup function"""
    print("SETUP: Setting up Wyckoff/SMC Trading System Project")
    print("=" * 60)
    
    # Create __init__.py files
    created_files = create_init_files()
    
    # Check project structure
    check_project_structure()
    
    # Create test runner
    create_test_runner()
    
    print("\n" + "=" * 60)
    print("SETUP SUMMARY")
    print("=" * 60)
    
    if created_files:
        print(f"SUCCESS: Created {len(created_files)} __init__.py files")
        print("SUCCESS: Project structure initialized")
        print("SUCCESS: Test runner created")
        
        print("\nNext Steps:")
        print("1. Run tests using:")
        print("   python run_tests.py")
        print("   OR")
        print("   python -m tests.performance_analytics_test_suite")
        print("\n2. If imports still fail, try:")
        print("   cd to your project root directory")
        print("   python -c \"import sys; print(sys.path)\"")
        print("   python -c \"from data_structures.ohlc import OHLCData; print('Import successful!')\"")
        
    else:
        print("INFO: All __init__.py files already exist")
        print("SUCCESS: Project structure looks good")
    
    print("\nTo run your tests:")
    print("   python run_tests.py")

if __name__ == "__main__":
    main()