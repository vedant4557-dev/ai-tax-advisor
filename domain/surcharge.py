# domain/surcharge.py

def calculate_surcharge(base_tax: float, gross_income: float) -> float:
    """
    Simplified surcharge logic.
    (You can enhance later)
    """

    if gross_income > 50000000:      # 5 Cr
        return round(base_tax * 0.37, 2)
    elif gross_income > 20000000:    # 2 Cr
        return round(base_tax * 0.25, 2)
    elif gross_income > 10000000:    # 1 Cr
        return round(base_tax * 0.15, 2)
    elif gross_income > 5000000:     # 50 Lakh
        return round(base_tax * 0.10, 2)
    else:
        return 0.0
