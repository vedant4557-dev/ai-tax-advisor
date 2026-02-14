# config/slabs_old.py

from typing import List, Tuple

Slab = List[Tuple[float, float]]

# Old Regime Slabs (FY 2024-25 & 2025-26 same for now)

OLD_REGIME_SLABS: Slab = [
    (250000, 0.00),
    (500000, 0.05),
    (1000000, 0.20),
    (float("inf"), 0.30),
]


def get_old_regime_slabs(tax_year: str) -> Slab:
    """
    Currently same slabs for both years.
    Future years can be split here.
    """
    if tax_year in ["2024-25", "2025-26"]:
        return OLD_REGIME_SLABS
    else:
        raise ValueError("Unsupported tax year for old regime")
