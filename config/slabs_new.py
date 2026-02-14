# config/slabs_new.py

from typing import List, Tuple

# Type alias
Slab = List[Tuple[float, float]]

# ---------------------------------------
# NEW REGIME SLABS – FY 2025-26
# 4L interval structure
# ---------------------------------------
NEW_REGIME_SLABS_2025_26: Slab = [
    (400000, 0.00),
    (800000, 0.05),
    (1200000, 0.10),
    (1600000, 0.15),
    (2000000, 0.20),
    (2400000, 0.25),
    (float("inf"), 0.30),
]


# ---------------------------------------
# NEW REGIME SLABS – FY 2024-25 (older)
# Keep for backward compatibility
# ---------------------------------------
NEW_REGIME_SLABS_2024_25: Slab = [
    (300000, 0.00),
    (600000, 0.05),
    (900000, 0.10),
    (1200000, 0.15),
    (1500000, 0.20),
    (float("inf"), 0.30),
]


def get_new_regime_slabs(tax_year: str) -> Slab:
    if tax_year == "2025-26":
        return NEW_REGIME_SLABS_2025_26
    elif tax_year == "2024-25":
        return NEW_REGIME_SLABS_2024_25
    else:
        raise ValueError("Unsupported tax year for new regime slabs")
