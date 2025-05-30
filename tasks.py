
from crewai import Task
from agents import TradingAgent

class TradingTask:
    def __init__(self):
        self.agent = TradingAgent()
        self.tasks = [
            self.create_market_structure_task(), 
            self.create_wyckoff_analysis_task(),
            self.create_smc_analysis_task(),
            self.create_entry_timing_task(),
            self.create_confluence_scoring_task(),
            self.create_risk_assessment_task(),
            self.create_session_filtering_task(),
            self.create_performance_analysis_task(),
            self.create_backtesting_validation_task(),
            self.create_data_coordination_task()
        ]

    def get_tasks(self):
        return self.tasks
    
    def create_market_structure_task(self):
        return Task(
            description="""Analyze the current market structure for US30, NAS100, SP500, 
            and USD major pairs on 1H and 15M timeframes. Identify:
            1. Overall market bias (bullish/bearish/neutral)
            2. Key swing highs and lows
            3. Critical support and resistance levels
            4. Trend changes and structural breaks
            5. Areas of institutional interest
            
            Provide a structured analysis that other agents can build upon.""",
            expected_output="""Market structure report containing:
            - Asset-by-asset bias analysis
            - Key level identification with confluence
            - Structural change alerts
            - Areas requiring deeper Wyckoff/SMC analysis"""
        )

    def create_wyckoff_analysis_task(self):
        return Task(
            description="""Based on the market structure analysis, identify Wyckoff 
            accumulation and distribution patterns. Look for:
            
            ACCUMULATION:
            - At least 3 tests of the selling climax
            - Spring formation and potential retests
            - Signs of composite operator absorption
            
            DISTRIBUTION:  
            - At least 3 tests of the buying climax
            - Upthrust formation and potential retests
            - Signs of composite operator distribution
            
            Focus on setups where spring/upthrust retests are forming.""",
            expected_output="""Wyckoff analysis report containing:
            - Identified accumulation/distribution phases
            - Spring and upthrust opportunities
            - Retest probability assessments
            - Entry level recommendations"""
        )

    def create_smc_analysis_task(self):
        return Task(
            description="""Identify Smart Money Concepts patterns that align with 
            the market structure and Wyckoff analysis:
            
            1. Order Blocks - Areas where institutions entered positions
            2. Fair Value Gaps - Imbalances requiring price to return
            3. Liquidity Sweeps - Stop hunts and manipulation patterns
            4. Breaker Blocks - Failed order blocks turned support/resistance
            
            Focus on patterns that confluence with Wyckoff setups.""",
            expected_output="""SMC analysis report containing:
            - Valid order blocks with entry/exit levels
            - Fair value gaps requiring mitigation
            - Liquidity sweep opportunities
            - SMC confluence with Wyckoff patterns"""
        )

    def create_entry_timing_task(self):
        return Task(
            description="""Using 5M and lower timeframes, identify precise entry 
            timing for the highest probability Wyckoff and SMC confluences:
            
            1. Spring retest entries with SMC confluence
            2. Upthrust retest entries with SMC confluence  
            3. Order block mitigation timing
            4. Fair value gap fill timing
            5. Optimal stop loss and take profit levels
            
            Only recommend entries with clear invalidation levels.""",
            expected_output="""Precision entry report containing:
            - Exact entry price levels
            - Stop loss placement reasoning
            - Take profit targets (minimum 1:5 RR)
            - Entry invalidation conditions
            - Timeframe-specific timing signals"""
        )

    def create_confluence_scoring_task(self):
        return Task(
            description="""Synthesize all analysis from previous agents and create 
            weighted confidence scores for each trading opportunity:
            
            Current Dynamic Weights:
            - Wyckoff Spring/Upthrust Retest: 40%
            - Order Block Alignment: 30%
            - Fair Value Gap: 20%  
            - Liquidity Sweep: 10%
            
            Assign confidence scores 1-10 and rank all opportunities.""",
            expected_output="""Confluence scoring report containing:
            - Ranked list of trade opportunities (1-10 confidence)
            - Detailed confluence breakdown for each setup
            - Weight justification for scoring
            - Recommended trade prioritization"""
        )

    def create_risk_assessment_task(self):
        return Task(
            description="""For each high-confidence trade opportunity, calculate:
            
            1. Position size based on 2% account risk
            2. Verify minimum 1:5 risk-reward ratio
            3. Adjust position size based on confluence confidence
            4. Account for correlations between simultaneous trades
            5. Final trade approval/rejection based on risk parameters
            
            No exceptions to risk management rules.""",
            expected_output="""Risk management report containing:
            - Approved trades with exact position sizes
            - Risk-reward calculations
            - Correlation adjustments
            - Rejected trades with reasoning
            - Maximum allowable exposure per asset"""
        )

    def create_session_filtering_task(self):
        return Task(
            description="""Apply final filtering based on market session timing:
            
            1. Verify trades occur during NY session (8 AM - 5 PM EST)
            2. Check for major news events that might affect execution
            3. Assess current market volatility and liquidity conditions
            4. Apply any session-specific filters
            5. Final approval for trade execution
            
            Only approve trades during optimal market conditions.""",
            expected_output="""Session filtering report containing:
            - Final approved trade list
            - Session timing confirmations  
            - Market condition assessments
            - News event considerations
            - Execution timing recommendations"""
        )

    def create_performance_analysis_task(self):
        return Task(
            description="""Every 5 completed trades, perform comprehensive analysis:
            
            1. Quantitative Performance Metrics:
            - Win/loss ratios, average win/loss amounts
            - Best/worst performing assets
            - Maximum consecutive losses
            - Time in trade analysis
            
            2. Qualitative LLM Analysis:
            - Why did winning trades succeed vs initial expectations?
            - What caused losing trades to fail?
            - Which confluence patterns performed best?
            - What market conditions favor our approach?
            
            3. System Optimization:
            - Recommend confluence weight adjustments
            - Suggest parameter improvements
            - Identify systematic weaknesses
            
            Trigger system recalibration with validated improvements.""",
            expected_output="""Performance analysis report containing:
            - Complete quantitative metrics dashboard
            - LLM-powered qualitative trade analysis
            - Confluence pattern effectiveness rankings
            - Recommended system parameter adjustments
            - Backtesting requirements for proposed changes"""
        )

    def create_backtesting_validation_task(self):
        return Task(
            description="""Before implementing any system changes recommended by 
            the Performance Analytics Agent:
            
            1. Test parameter changes on 6 months of historical data
            2. Validate statistical significance of improvements
            3. Check for overfitting to recent market conditions
            4. Assess robustness across different market regimes
            5. Approve or reject proposed changes
            
            Only approve changes that show consistent improvement.""",
            expected_output="""Backtesting validation report containing:
            - Historical performance of proposed changes
            - Statistical significance tests
            - Robustness analysis across market conditions
            - Approved/rejected change recommendations
            - Implementation timeline for approved changes"""
        )

    # def create_data_coordination_task(self):
    #     return Task(
    #         description="""Coordinate all data operations for the 3-minute scanning cycle:
            
    #         1. Fetch fresh data from Twelve Data, TradingView, Yahoo Finance
    #         2. Ensure data quality and handle missing/corrupted data
    #         3. Synchronize data across all agents
    #         4. Monitor data feed health and switch sources if needed
    #         5. Prepare data in formats required by each agent
            
    #         Execute every 3 minutes during market hours.""",
    #         expected_output="""Data coordination report containing:
    #         - Data feed status for all sources
    #         - Data quality metrics
    #         - Synchronized dataset for agent consumption
    #         - Any data issues and resolutions
    #         - Next scan cycle timing"""
    #     )
        
        # task():
        # return Task(
        #     description="""Before implementing any system changes recommended by 
        #     the Performance Analytics Agent:
            
        #     1. Test parameter changes on 6 months of historical data
        #     2. Validate statistical significance of improvements
        #     3. Check for overfitting to recent market conditions
        #     4. Assess robustness across different market regimes
        #     5. Approve or reject proposed changes
            
        #     Only approve changes that show consistent improvement.""",
        #     expected_output="""Backtesting validation report containing:
        #     - Historical performance of proposed changes
        #     - Statistical significance tests
        #     - Robustness analysis across market conditions
        #     - Approved/rejected change recommendations
        #     - Implementation timeline for approved changes""",
        #     agent=create_backtesting_agent()
        # )

    def create_data_coordination_task(self):
        return Task(
            description="""Coordinate all data operations for the 3-minute scanning cycle:
            
            1. Fetch fresh data from Twelve Data, TradingView, Yahoo Finance
            2. Ensure data quality and handle missing/corrupted data
            3. Synchronize data across all agents
            4. Monitor data feed health and switch sources if needed
            5. Prepare data in formats required by each agent
            
            Execute every 3 minutes during market hours.""",
            expected_output="""Data coordination report containing:
            - Data feed status for all sources
            - Data quality metrics
            - Synchronized dataset for agent consumption
            - Any data issues and resolutions
            - Next scan cycle timing""",
            agent=self.agent.create_data_orchestrator_agent()
        )