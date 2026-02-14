# domain/surcharge.py

def calculate_surcharge(taxable_income: float, base_tax: float) -> float:
    """
    Calculates surcharge based on income thresholds.
    """

    if taxable_income > 50000000:       # > 5 Cr
        rate = 0.37
    elif taxable_income > 20000000:     # > 2 Cr
        rate = 0.25
    elif taxable_income > 10000000:     # > 1 Cr
        rate = 0.15
    elif taxable_income > 5000000:      # > 50 L
        rate = 0.10
    else:
        rate = 0.0

    return base_tax * rate
