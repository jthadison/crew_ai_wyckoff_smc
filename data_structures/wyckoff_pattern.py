from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Tuple


@dataclass
class WyckoffPattern:
    """Wyckoff pattern detection result"""
    pattern_type: str  # 'ACCUMULATION', 'DISTRIBUTION', 'MARKUP', 'MARKDOWN'
    phase: str  # 'PS', 'SC', 'AR', 'ST', 'BC', 'AD', 'UTAD', etc.
    confidence: float  # 0-100
    start_time: datetime
    end_time: datetime
    key_levels: Dict[str, float]
    description: str