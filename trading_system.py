
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from typing import Dict, List, Any
import pandas as pd
from datetime import datetime, timedelta
import json

from agents import create_market_structure_agent, create_wyckoff_agent, create_smc_agent, create_entry_precision_agent, create_confluence_scoring_agent, create_risk_management_agent, create_session_filter_agent, create_performance_analytics_agent, create_backtesting_agent

#from crew import create_backtesting_validation_task, create_performance_analysis_task, create_trading_crew
#from crew import create_backtesting_agent, create_backtesting_validation_task, create_confluence_scoring_agent, create_confluence_scoring_task, create_data_coordination_task, create_data_orchestrator_agent, create_entry_precision_agent, create_entry_timing_task, create_market_structure_agent, create_market_structure_task, create_performance_analysis_task, create_performance_analytics_agent, create_risk_assessment_task, create_risk_management_agent, create_session_filter_agent, create_session_filtering_task, create_smc_agent, create_smc_analysis_task, create_wyckoff_agent, create_wyckoff_analysis_task

class TradingSystemController:
    def __init__(self):
        crew = Crew()
        self.crew, self.agents = create_trading_crew()
        self.trade_count = 0
        self.performance_data = []
        self.system_parameters = {
            'wyckoff_weight': 40,
            'ob_weight': 30,
            'fvg_weight': 20,
            'liq_weight': 10
        }
    
    def run_scanning_cycle(self):
        """Execute one 3-minute scanning cycle"""
        try:
            result = self.crew.kickoff()
            return result
        except Exception as e:
            print(f"Scanning cycle error: {e}")
            return None
    
    def record_trade_result(self, trade_data: Dict):
        """Record completed trade for performance analysis"""
        self.performance_data.append(trade_data)
        self.trade_count += 1
        
        # Trigger performance analysis every 5 trades
        if self.trade_count % 5 == 0:
            self.run_performance_analysis()
    
    def run_performance_analysis(self):
        """Run performance analysis and system optimization"""
        perf_task = create_performance_analysis_task()
        backtest_task = create_backtesting_validation_task()
        
        # Performance analysis
        perf_result = perf_task.execute()
        
        # Backtesting validation of proposed changes
        backtest_result = backtest_task.execute()
        
        # Update system parameters if validated
        if backtest_result.get('approved_changes'):
            self.update_system_parameters(backtest_result['approved_changes'])
    
    def update_system_parameters(self, new_parameters: Dict):
        """Update system parameters after validation"""
        self.system_parameters.update(new_parameters)
        
        # Update confluence agent with new weights
        confluence_agent = self.agents['confluence']
        confluence_agent.system_template = confluence_agent.system_template.format(
            **self.system_parameters
        )
        
    def create_trading_crew():
        """Create the complete trading crew with all agents and tasks"""
    
        # Create all agents
        agents = {
            'market_structure': create_market_structure_agent(),
            'wyckoff': create_wyckoff_agent(),
            'smc': create_smc_agent(),
            'entry_timing': create_entry_precision_agent(),
            'confluence': create_confluence_scoring_agent(),
            'risk_mgmt': create_risk_management_agent(),
            'session_filter': create_session_filter_agent(),
            'performance': create_performance_analytics_agent(),
            'backtesting': create_backtesting_agent(),
            'data_coord': create_data_orchestrator_agent()
        }
        
        # Create all tasks
        tasks = [
            create_data_coordination_task(),      # Always first
            create_market_structure_task(),       # HTF analysis
            create_wyckoff_analysis_task(),       # Wyckoff patterns
            create_smc_analysis_task(),           # SMC patterns  
            create_entry_timing_task(),           # Precise entries
            create_confluence_scoring_task(),     # Score & rank
            create_risk_assessment_task(),        # Risk management
            create_session_filtering_task(),      # Final filtering
            # Performance and backtesting run separately every 5 trades
        ]
        
        # Create the crew
        trading_crew = Crew(
            agents=list(agents.values()),
            tasks=tasks,
            process=Process.sequential,
            memory=True,
            cache=True,
            max_rpm=100,
            share_crew=False
        )
        
        return trading_crew, agents