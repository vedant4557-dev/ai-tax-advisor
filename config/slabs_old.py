# config/slabs_old.py

from typing import List, Tuple

Slab = List[Tuple[float, float]]

OLD_REGIME_SLABS: Slab = [
    (250000, 0.00),
    (500000, 0.05),
    (1000000, 0.20),
    (float("inf"), 0.30),
]

def get_old_regime_slabs(tax_year: str) -> Slab:
    return OLD_REGIME_SLABS
    