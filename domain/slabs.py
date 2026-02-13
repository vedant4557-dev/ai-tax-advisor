# tax_engine/slabs.py

from typing import List, Tuple


class SlabCalculator:
    def __init__(self, slabs: List[Tuple[float, float]]):
        """
        slabs format:
        [
            (upper_limit, rate),
            (upper_limit, rate),
            ...
        ]

        upper_limit = income upper bound
        rate = tax rate (0.05 = 5%)
        """
        self.slabs = slabs

    def calculate(self, taxable_income: float) -> float:
        tax = 0.0
        previous_limit = 0.0

        for upper_limit, rate in self.slabs:
            if taxable_income <= previous_limit:
                break
            taxable_amount = min(taxable_income, upper_limit) - previous_limit
            tax += taxable_amount * rate
            previous_limit = upper_limit

        return max(tax, 0.0)
from typing import List, Tuple

class SlabCalculator:
    def __init__(self, slabs: List[Tuple[float, float]]):
        self.slabs = slabs

    def calculate(self, taxable_income: float) -> float:
        tax = 0.0
        previous_limit = 0.0

        for upper_limit, rate in self.slabs:
            if taxable_income <= previous_limit:
                break

            taxable_amount = min(taxable_income, upper_limit) - previous_limit
            tax += taxable_amount * rate
            previous_limit = upper_limit

        return max(tax, 0.0)
