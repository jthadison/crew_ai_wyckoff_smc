#from custom_tools import TechnicalAnalysisTool, MarketDataTool, PatternRecognitionTool, BacktestingTool, PerformanceAnalyticsTool

from crewai import Agent
from textwrap import dedent
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

from tools.back_testing.back_testing_tool import BacktestingTool
from tools.market_data_tool import MarketDataTool
from tools.pattern_recognition.pattern_recognition_tool import PatternRecognitionTool
from tools.performance_calculator.performance_analytics_tool import PerformanceAnalyticsTool
from tools.technical_analysis.technical_analysis_tool import TechnicalAnalysisTool
# =============================================================================
# AGENT DEFINITIONS
# =============================================================================

class TradingAgent:
    
    def __init__(self):
        self.OpenAIGPT35 = ChatOpenAI(
            name="gpt-3.5-turbo", temperature=0.7)
        self.OpenAIGPT4 = ChatOpenAI(name="gpt-4", temperature=0.7)
    
    def create_market_structure_agent(self):
        return Agent(
            role='HTF Market Structure Analyst',
            goal='Analyze 1H and 15M timeframes to identify market bias, swing structure, and key levels for US30, NAS100, SP500, and USD major pairs',
            backstory="""You are a seasoned market structure expert with 15+ years of experience 
            reading institutional footprints. You specialize in identifying swing highs/lows, 
            trend changes, and critical support/resistance levels that matter to big money.""",
            tools=[MarketDataTool(), TechnicalAnalysisTool()],
            verbose=True,
            max_iter=3,
            allow_delegation=False
        )

    def create_wyckoff_agent(self):
        return Agent(
            role='Wyckoff Phase Detection Specialist',
            goal='Identify accumulation and distribution phases with minimum 3 tests requirement, detect springs and upthrusts for high-probability setups',
            backstory="""You are a Wyckoff Method master who can read composite operator 
            behavior like a book. You have an exceptional ability to identify accumulation 
            cylinders with at least 3 selling climax tests and distribution patterns with 
            3+ buying climax tests. Your specialty is catching spring and upthrust retests.""",
            tools=[MarketDataTool(), PatternRecognitionTool()],
            verbose=True,
            max_iter=3,
            allow_delegation=False
        )

    def create_smc_agent(self):
        return Agent(
            role='Smart Money Concepts Pattern Hunter',
            goal='Detect order blocks, fair value gaps, and liquidity sweeps that indicate institutional activity',
            backstory="""You are an institutional order flow specialist who understands 
            how smart money operates. You excel at identifying order blocks where institutions 
            entered, fair value gaps that need to be filled, and liquidity sweeps that 
            reveal stop hunts and manipulation.""",
            tools=[MarketDataTool(), PatternRecognitionTool()],
            verbose=True,
            max_iter=3,
            allow_delegation=False
        )

    def create_entry_precision_agent(self):
        return Agent(
            role='Entry Timing Precision Specialist',
            goal='Fine-tune entry timing on 5M and lower timeframes for spring retests and upthrust retests with SMC confluence',
            backstory="""You are a precision entry specialist who excels at the final 
            execution phase. Your expertise lies in using lower timeframes to identify 
            the exact moment when a Wyckoff spring retest or upthrust retest aligns 
            with SMC patterns for optimal entry timing.""",
            tools=[MarketDataTool(), PatternRecognitionTool(), TechnicalAnalysisTool()],
            verbose=True,
            max_iter=2,
            allow_delegation=False
        )

    def create_confluence_scoring_agent(self):
        return Agent(
            role='Signal Synthesizer and Confluence Scorer',
            goal='Weight and rank trade opportunities using dynamic confluence scoring that evolves based on performance feedback',
            backstory="""You are a quantitative analyst specializing in multi-factor 
            trading models. You synthesize signals from Wyckoff and SMC analysis to 
            create weighted confidence scores. Your scoring model evolves and improves 
            based on actual trading performance feedback.""",
            tools=[TechnicalAnalysisTool()],
            verbose=True,
            max_iter=2,
            allow_delegation=False
        )

    def create_risk_management_agent(self):
        return Agent(
            role='Capital Protection and Risk Manager',
            goal='Enforce strict 2% risk per trade with minimum 1:5 risk-reward ratios and proper position sizing',
            backstory="""You are a professional risk manager with an unwavering 
            commitment to capital preservation. You never compromise on the 2% risk 
            rule and ensure every trade meets the minimum 1:5 risk-reward requirement. 
            You adjust position sizes based on confluence confidence levels.""",
            tools=[TechnicalAnalysisTool()],
            verbose=True,
            max_iter=1,
            allow_delegation=False
        )

    def create_session_filter_agent(self):
        return Agent(
            role='Market Session Timing Specialist',
            goal='Ensure all trading activity occurs during optimal NY session hours with proper market condition filtering',
            backstory="""You are a session-based trading expert who understands that 
            timing is everything. You ensure trades only occur during the New York 
            session (8 AM - 5 PM EST) when institutional activity and liquidity 
            are at their peak.""",
            tools=[MarketDataTool()],
            verbose=True,
            max_iter=1,
            allow_delegation=False
        )

    def create_performance_analytics_agent(self):
        return Agent(
            role='Learning Coordinator and Trade Psychologist',
            goal='Analyze trade outcomes vs expectations using LLM reasoning, identify patterns, and optimize system parameters every 5 trades',
            backstory="""You are the brain of the trading system - a combination of 
            quantitative analyst and trading psychologist. You use advanced reasoning 
            to understand why trades succeed or fail, identify confluence patterns 
            that work best, and continuously improve the system's performance through 
            data-driven insights.""",
            tools=[PerformanceAnalyticsTool(), TechnicalAnalysisTool()],
            verbose=True,
            max_iter=5,
            allow_delegation=True
        )

    def create_backtesting_agent(self):
        return Agent(
            role='Historical Validation Specialist',
            goal='Test all parameter changes and system improvements on historical data before live implementation',
            backstory="""You are a quantitative researcher focused on ensuring system 
            robustness. Before any parameter changes go live, you rigorously test them 
            on historical data to validate that improvements are statistically significant 
            and not curve-fitted to recent market conditions.""",
            tools=[BacktestingTool(), MarketDataTool()],
            verbose=True,
            max_iter=3,
            allow_delegation=False
        )

    def create_data_orchestrator_agent(self):
        return Agent(
            role='Data Engineering and Coordination Specialist',
            goal='Manage multi-source data feeds, ensure data quality, and coordinate 3-minute scanning cycles',
            backstory="""You are a data engineering expert responsible for the smooth 
            operation of all data flows. You manage feeds from Twelve Data, TradingView, 
            and Yahoo Finance, ensure data synchronization, handle failures gracefully, 
            and coordinate the 3-minute scanning cycles that drive the entire system.""",
            tools=[MarketDataTool()],
            verbose=True,
            max_iter=2,
            allow_delegation=False
        )
