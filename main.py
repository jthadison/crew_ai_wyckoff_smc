
from crewai import Agent, Task, Crew, Process
from typing import Dict,  Any, Optional
from datetime import datetime
#from custom_tools import MarketDataTool, PatternRecognitionTool, TechnicalAnalysisTool, BacktestingTool, PerformanceAnalyticsTool
#from agents import create_market_structure_agent, create_wyckoff_agent, create_smc_agent, create_entry_precision_agent, create_confluence_scoring_agent, create_risk_management_agent, create_session_filter_agent, create_performance_analytics_agent, create_backtesting_agent

#from crew import create_backtesting_validation_task, create_performance_analysis_task, create_trading_crew
#from crew import create_backtesting_agent, create_backtesting_validation_task, create_confluence_scoring_agent, create_confluence_scoring_task, create_data_coordination_task, create_data_orchestrator_agent, create_entry_precision_agent, create_entry_timing_task, create_market_structure_agent, create_market_structure_task, create_performance_analysis_task, create_performance_analytics_agent, create_risk_assessment_task, create_risk_management_agent, create_session_filter_agent, create_session_filtering_task, create_smc_agent, create_smc_analysis_task, create_wyckoff_agent, create_wyckoff_analysis_task
from tools.market_data_tool import MarketDataTool
from agents import TradingAgent
from tasks import TradingTask
from dotenv import load_dotenv

from tools.pattern_recognition.pattern_recognition_tool import PatternRecognitionTool
from tools.technical_analysis.technical_analysis_tool import TechnicalAnalysisTool

load_dotenv()

class SimpleTradingSystem:
    """Simplified trading system that avoids type conflicts"""
    
    def __init__(self):
        self.market_data_tool = MarketDataTool()
        self.pattern_tool = PatternRecognitionTool()
        self.tech_analysis_tool = TechnicalAnalysisTool()
        
        # System parameters
        self.confluence_weights = {
            'wyckoff': 40,
            'order_block': 30,
            'fvg': 20,
            'liquidity_sweep': 10
        }
        
        self.trade_count = 0
        self.performance_data = []
    
    def create_market_analyst(self) -> Agent:
        """Create market structure analyst"""
        return Agent(
            role="Market Structure Analyst",
            goal="Analyze market structure on 1H and 15M timeframes for US30, NAS100, SP500, and USD pairs",
            backstory="Expert in reading institutional footprints and market structure",
            tools=[self.market_data_tool, self.tech_analysis_tool],
            verbose=True,
            allow_delegation=False
        )
    
    def create_wyckoff_specialist(self) -> Agent:
        """Create Wyckoff pattern specialist"""
        return Agent(
            role="Wyckoff Pattern Specialist",
            goal="Identify accumulation/distribution phases with 3+ tests and spring/upthrust retests",
            backstory="Master of Wyckoff methodology and composite operator behavior",
            tools=[self.pattern_tool, self.market_data_tool],
            verbose=True,
            allow_delegation=False
        )
    
    def create_smc_analyst(self) -> Agent:
        """Create Smart Money Concepts analyst"""
        return Agent(
            role="Smart Money Analyst",
            goal="Detect order blocks, fair value gaps, and liquidity sweeps",
            backstory="Specialist in institutional order flow and smart money patterns",
            tools=[self.pattern_tool, self.market_data_tool],
            verbose=True,
            allow_delegation=False
        )
    
    def create_risk_manager(self) -> Agent:
        """Create risk management agent"""
        return Agent(
            role="Risk Manager",
            goal="Enforce 2% risk per trade with minimum 1:5 risk-reward ratios",
            backstory="Professional risk manager focused on capital preservation",
            tools=[self.tech_analysis_tool],
            verbose=True,
            allow_delegation=False
        )
    
    def create_market_analysis_task(self) -> Task:
        """Create market structure analysis task"""
        return Task(
            description="""
            Analyze current market structure for US30, NAS100, SP500, and USD major pairs:
            1. Identify overall market bias (bullish/bearish/neutral)
            2. Mark key swing highs and lows
            3. Identify critical support and resistance levels
            4. Detect trend changes and structural breaks
            
            Focus on 1H and 15M timeframes for institutional perspective.
            """,
            expected_output="Market structure report with bias, key levels, and institutional areas of interest"
        )
    
    def create_wyckoff_task(self) -> Task:
        """Create Wyckoff analysis task"""
        return Task(
            description="""
            Identify Wyckoff accumulation and distribution patterns:
            
            For ACCUMULATION:
            - Look for at least 3 tests of the selling climax
            - Identify spring formation and potential retests
            - Assess composite operator absorption signs
            
            For DISTRIBUTION:
            - Look for at least 3 tests of the buying climax  
            - Identify upthrust formation and potential retests
            - Assess composite operator distribution signs
            
            Prioritize setups where spring/upthrust retests are forming.
            """,
            expected_output="Wyckoff analysis with identified phases, spring/upthrust opportunities, and entry recommendations"
        )
    
    def create_smc_task(self) -> Task:
        """Create SMC analysis task"""
        return Task(
            description="""
            Identify Smart Money Concepts patterns:
            1. Order Blocks - Areas where institutions entered positions
            2. Fair Value Gaps - Price imbalances requiring mitigation
            3. Liquidity Sweeps - Stop hunts and manipulation patterns
            4. Breaker Blocks - Failed order blocks turned support/resistance
            
            Focus on patterns that confluence with Wyckoff setups.
            """,
            expected_output="SMC analysis with order blocks, FVGs, liquidity sweeps, and confluence opportunities"
        )
    
    def create_risk_task(self) -> Task:
        """Create risk management task"""
        return Task(
            description="""
            Apply risk management to identified opportunities:
            1. Calculate position size based on 2% account risk
            2. Verify minimum 1:5 risk-reward ratio
            3. Adjust sizing based on confluence confidence
            4. Check for correlation between simultaneous trades
            5. Final trade approval/rejection
            
            No exceptions to risk management rules.
            """,
            expected_output="Risk-managed trade list with position sizes, R:R ratios, and final approvals"
        )
    
    def run_analysis_cycle(self) -> Optional[str]:
        """Run one complete analysis cycle"""
        
        try:
            # Create agents
            market_agent = self.create_market_analyst()
            wyckoff_agent = self.create_wyckoff_specialist()
            smc_agent = self.create_smc_analyst()
            risk_agent = self.create_risk_manager()
            
            # Create tasks
            market_task = self.create_market_analysis_task()
            wyckoff_task = self.create_wyckoff_task()
            smc_task = self.create_smc_task()
            risk_task = self.create_risk_task()
            
            # Create crew - explicit instantiation to avoid type issues
            crew = Crew(
                agents=[market_agent, wyckoff_agent, smc_agent, risk_agent],
                tasks=[market_task, wyckoff_task, smc_task, risk_task],
                process=Process.sequential,
                verbose=True
            )
            
            print("🔄 Starting analysis cycle...")
            result = crew.kickoff()
            print("✅ Analysis cycle completed")
            
            # Handle CrewOutput properly
            if hasattr(result, 'raw'):
                return str(result.raw)
            else:
                return str(result)
            
        except Exception as e:
            print(f"❌ Error in analysis cycle: {e}")
            return None
    
    def record_trade(self, trade_data: Dict[str, Any]) -> None:
        """Record a completed trade"""
        self.performance_data.append(trade_data)
        self.trade_count += 1
        
        print(f"📊 Trade recorded: {trade_data.get('result', 'unknown')}")
        
        # Trigger performance analysis every 5 trades
        if self.trade_count % 5 == 0:
            self.analyze_performance()
    
    def analyze_performance(self) -> None:
        """Analyze recent performance and adjust parameters"""
        
        print(f"🧠 Analyzing performance after {self.trade_count} trades...")
        
        # Simple performance analysis
        recent_trades = self.performance_data[-5:]
        wins = [t for t in recent_trades if t.get('result') == 'win']
        win_rate = len(wins) / len(recent_trades) * 100
        
        print(f"📈 Recent win rate: {win_rate:.1f}%")
        
        # Simple parameter adjustment based on performance
        if win_rate > 70:
            # System performing well, small adjustments
            print("🎯 System performing well - minor optimizations")
        elif win_rate < 50:
            # System needs adjustment
            print("⚠️ System needs adjustment - rebalancing weights")
            # Adjust confluence weights
            self.confluence_weights['wyckoff'] = min(45, self.confluence_weights['wyckoff'] + 2)
            self.confluence_weights['order_block'] = max(25, self.confluence_weights['order_block'] - 1)
        
        print(f"🔧 Updated weights: {self.confluence_weights}")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        return {
            'trade_count': self.trade_count,
            'confluence_weights': self.confluence_weights,
            'last_analysis': datetime.now().isoformat(),
            'performance_data_points': len(self.performance_data)
        }

    def main(self):
        """Example usage of the simplified trading system"""
        
        print("🚀 Starting Simplified CrewAI Trading System")
        print("=" * 50)
        
        # Initialize system
        #trading_system = SimpleTradingSystem()
        
        # Run analysis cycle
        result = self.run_analysis_cycle()
        
        if result:
            print(f"\n📋 Analysis Result:\n{result}")
        
        # Simulate some trades for demonstration
        demo_trades = [
            {'result': 'win', 'pnl': 450, 'asset': 'US30', 'confidence': 8.5},
            {'result': 'win', 'pnl': 320, 'asset': 'NAS100', 'confidence': 7.8},
            {'result': 'loss', 'pnl': -90, 'asset': 'EURUSD', 'confidence': 6.5},
            {'result': 'win', 'pnl': 380, 'asset': 'US30', 'confidence': 8.2},
            {'result': 'win', 'pnl': 290, 'asset': 'SP500', 'confidence': 7.5}
        ]
        
        print(f"\n🎯 Simulating trade results...")
        for i, trade in enumerate(demo_trades, 1):
            print(f"Trade {i}: {trade['result']} - ${trade['pnl']} ({trade['asset']})")
            #trading_system.record_trade(trade)
            self.record_trade(trade)
        # Show final system status
        #status = trading_system.get_system_status()
        status = self.get_system_status()
        print(f"\n📊 Final System Status:")
        for key, value in status.items():
            print(f"   {key}: {value}")

if __name__ == "__main__":
    system = SimpleTradingSystem()
    system.main()