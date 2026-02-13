def apply_rebate(tax: float, taxable_income: float) -> float:
    if taxable_income <= 700000:
        return 0.0
    return tax
