from typing import Optional
from dataclasses import dataclass

@dataclass
class DeliveryResult:
    delivery_type: str  # ['no_ball', 'wide_ball', 'fair_delivery', 'good_delivery']
    stroke_type: str    # ['miss', 'dot', 'hit', 'slog']
    runs_scored: int
    extras: int
    is_wicket: bool
    dismissal_type: Optional[str] = None  # ['bowled', 'lbw', 'stumped', 'caught']
    fielder_involved: Optional[str] = None  # ['wicketkeeper', 'fielder']
