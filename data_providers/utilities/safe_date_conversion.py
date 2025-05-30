from datetime import datetime
from typing import Optional

import pandas as pd


class SafeDateConversion:
    @staticmethod
    def safe_datetime_conversion(timestamp) -> Optional[datetime]:
        """Safely convert various timestamp formats to datetime"""
        
        if timestamp is None:
            return None
        
        # Already a datetime object
        if isinstance(timestamp, datetime):
            return timestamp
        
        # Pandas Timestamp
        if hasattr(timestamp, 'to_pydatetime'):
            try:
                return timestamp.to_pydatetime()
            except Exception:
                pass
        
        # Try pandas to_datetime
        if hasattr(timestamp, 'to_datetime'):
            try:
                return timestamp.to_datetime()
            except Exception:
                pass
        
        # String conversion
        if isinstance(timestamp, str):
            try:
                # Try common formats
                for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%Y-%m-%d %H:%M:%S%z']:
                    try:
                        return datetime.strptime(timestamp, fmt)
                    except ValueError:
                        continue
            except Exception:
                pass
        
        # Use pandas to_datetime as fallback
        try:
            dt = pd.to_datetime(timestamp)
            if hasattr(dt, 'to_pydatetime'):
                return dt.to_pydatetime()
            else:
                return dt
        except Exception:
            pass
        
        # Final fallback - return current datetime with warning
        print(f"Warning: Could not convert timestamp {timestamp} to datetime, using current time")
        return datetime.now()
    @staticmethod
    def safe_float_conversion(value, default: float = 0.0) -> float:
        """Safely convert value to float, handling NaN and None"""
        
        if value is None:
            return default
        
        if pd.isna(value):
            return default
        
        try:
            return float(value)
        except (ValueError, TypeError):
            return default