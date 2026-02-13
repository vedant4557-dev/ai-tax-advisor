class Surcharge:

    @staticmethod
    def calculate_surcharge(tax: float, taxable_income: float) -> float:
        """
        Apply surcharge based on taxable income.
        """

        if taxable_income > 5_00_00_000:
            rate = 0.37
        elif taxable_income > 2_00_00_000:
            rate = 0.25
        elif taxable_income > 1_00_00_000:
            rate = 0.15
        elif taxable_income > 50_00_000:
            rate = 0.10
        else:
            rate = 0.0

        return tax * rate
