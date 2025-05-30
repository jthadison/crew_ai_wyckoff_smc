from agents import TradingAgent
from tasks import TradingTask
from crewai import Crew, Process

class TradingCrewConfig:
    def create_trading_crew(self):
        """Create the complete trading crew with all agents and tasks"""
        self.agents = TradingAgent()
        self.tasks = TradingTask()
        try:
            # Create all agents individually to avoid list type issues
            data_coord_agent = self.agents.create_data_orchestrator_agent()
            market_structure_agent = self.agents.create_market_structure_agent()
            wyckoff_agent = self.agents.create_wyckoff_agent()
            smc_agent = self.agents.create_smc_agent()
            entry_agent = self.agents.create_entry_precision_agent()
            confluence_agent = self.agents.create_confluence_scoring_agent()
            risk_agent = self.agents.create_risk_management_agent()
            session_agent = self.agents.create_session_filter_agent()
            
            # Create all tasks
            data_task = self.tasks.create_data_coordination_task()
            market_task = self.tasks.create_market_structure_task()
            wyckoff_task = self.tasks.create_wyckoff_analysis_task()
            smc_task = self.tasks.create_smc_analysis_task()
            entry_task = self.tasks.create_entry_timing_task()
            confluence_task = self.tasks.create_confluence_scoring_task()
            risk_task = self.tasks.create_risk_assessment_task()
            session_task = self.tasks.create_session_filtering_task()
            
            # Create the crew with explicit agent and task assignment
            trading_crew = Crew(
                agents=[
                    data_coord_agent,
                    market_structure_agent,
                    wyckoff_agent,
                    smc_agent,
                    entry_agent,
                    confluence_agent,
                    risk_agent,
                    session_agent
                ],
                tasks=[
                    data_task,
                    market_task,
                    wyckoff_task,
                    smc_task,
                    entry_task,
                    confluence_task,
                    risk_task,
                    session_task
                ],
                process=Process.sequential,
                verbose=True
            )
            
            # Create agents dictionary for easy access
            agents_dict = {
                'data_coord': data_coord_agent,
                'market_structure': market_structure_agent,
                'wyckoff': wyckoff_agent,
                'smc': smc_agent,
                'entry_timing': entry_agent,
                'confluence': confluence_agent,
                'risk_mgmt': risk_agent,
                'session_filter': session_agent
            }
            
            return trading_crew, agents_dict
            
        except Exception as e:
            print(f"Error creating trading crew: {e}")
            print("This might be a CrewAI version compatibility issue.")
            print("Try: pip install --upgrade crewai")
            raise