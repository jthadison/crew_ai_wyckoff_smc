from typing import Dict, List
import numpy as np

class TechnicalIndicators:
    """Core technical indicators calculations"""
    
    @staticmethod
    def sma(data: List[float], period: int) -> List[float]:
        """Simple Moving Average"""
        if len(data) < period:
            return [np.nan] * len(data)
        
        result = []
        for i in range(len(data)):
            if i < period - 1:
                result.append(np.nan)
            else:
                result.append(np.mean(data[i-period+1:i+1]))
        return result
    
    @staticmethod
    def ema(data: List[float], period: int) -> List[float]:
        """Exponential Moving Average"""
        if len(data) < period:
            return [np.nan] * len(data)
        
        alpha = 2.0 / (period + 1)
        result = []
        
        # First value is SMA
        first_sma = np.mean(data[:period])
        result.extend([np.nan] * (period - 1))
        result.append(first_sma)
        
        # Calculate EMA for remaining values
        for i in range(period, len(data)):
            ema_val = alpha * data[i] + (1 - alpha) * result[-1]
            result.append(ema_val)
        
        return result
    
    @staticmethod
    def rsi(data: List[float], period: int = 14) -> List[float]:
        """Relative Strength Index"""
        if len(data) < period + 1:
            return [np.nan] * len(data)
        
        changes = [data[i] - data[i-1] for i in range(1, len(data))]
        gains = [max(0, change) for change in changes]
        losses = [max(0, -change) for change in changes]
        
        avg_gain = np.mean(gains[:period])
        avg_loss = np.mean(losses[:period])
        
        result = [np.nan] * (period + 1)
        
        if avg_loss == 0:
            result.append(100)
        else:
            rs = avg_gain / avg_loss
            result.append(float(100 - (100 / (1 + rs))))
        
        # Calculate RSI for remaining values
        for i in range(period + 1, len(data)):
            gain = max(0, data[i] - data[i-1])
            loss = max(0, data[i-1] - data[i])
            
            avg_gain = (avg_gain * (period - 1) + gain) / period
            avg_loss = (avg_loss * (period - 1) + loss) / period
            
            if avg_loss == 0:
                result.append(100)
            else:
                rs = avg_gain / avg_loss
                result.append(float(100 - (100 / (1 + rs))))
        
        return result
    
    @staticmethod
    def macd(data: List[float], fast: int = 12, slow: int = 26, signal: int = 9) -> Dict[str, List[float]]:
        """MACD (Moving Average Convergence Divergence)"""
        ema_fast = TechnicalIndicators.ema(data, fast)
        ema_slow = TechnicalIndicators.ema(data, slow)
        
        macd_line = []
        for i in range(len(data)):
            if np.isnan(ema_fast[i]) or np.isnan(ema_slow[i]):
                macd_line.append(np.nan)
            else:
                macd_line.append(ema_fast[i] - ema_slow[i])
        
        signal_line = TechnicalIndicators.ema(macd_line, signal)
        
        histogram = []
        for i in range(len(macd_line)):
            if np.isnan(macd_line[i]) or np.isnan(signal_line[i]):
                histogram.append(np.nan)
            else:
                histogram.append(macd_line[i] - signal_line[i])
        
        return {
            'macd': macd_line,
            'signal': signal_line,
            'histogram': histogram
        }
    
    @staticmethod
    def bollinger_bands(data: List[float], period: int = 20, std_dev: float = 2.0) -> Dict[str, List[float]]:
        """Bollinger Bands"""
        sma_values = TechnicalIndicators.sma(data, period)
        
        upper_band = []
        lower_band = []
        
        for i in range(len(data)):
            if i < period - 1 or np.isnan(sma_values[i]):
                upper_band.append(np.nan)
                lower_band.append(np.nan)
            else:
                window_data = data[i-period+1:i+1]
                std = np.std(window_data, ddof=1)
                upper_band.append(sma_values[i] + (std_dev * std))
                lower_band.append(sma_values[i] - (std_dev * std))
        
        return {
            'upper': upper_band,
            'middle': sma_values,
            'lower': lower_band
        }
    
    @staticmethod
    def stochastic(highs: List[float], lows: List[float], closes: List[float], 
                   k_period: int = 14, d_period: int = 3) -> Dict[str, List[float]]:
        """Stochastic Oscillator"""
        k_values = []
        
        for i in range(len(closes)):
            if i < k_period - 1:
                k_values.append(np.nan)
            else:
                window_high = max(highs[i-k_period+1:i+1])
                window_low = min(lows[i-k_period+1:i+1])
                
                if window_high == window_low:
                    k_values.append(50)
                else:
                    k_val = ((closes[i] - window_low) / (window_high - window_low)) * 100
                    k_values.append(k_val)
        
        d_values = TechnicalIndicators.sma(k_values, d_period)
        
        return {
            'k': k_values,
            'd': d_values
        }