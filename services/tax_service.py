class TaxService:

    # ----------------------------
    # FY 2025-26 NEW REGIME SLABS
    # ----------------------------
    NEW_SLABS = [
        (400000, 0.00),
        (800000, 0.05),
        (1200000, 0.10),
        (1600000, 0.15),
        (2000000, 0.20),
        (2400000, 0.25),
        (float("inf"), 0.30),
    ]

    # ----------------------------
    # OLD REGIME SLABS
    # ----------------------------
    OLD_SLABS = [
        (250000, 0.00),
        (500000, 0.05),
        (1000000, 0.20),
        (float("inf"), 0.30),
    ]

    # ----------------------------
    # Tax Calculator
    # ----------------------------
    @staticmethod
    def _calculate_tax(income, slabs):
        tax = 0
        previous_limit = 0

        for limit, rate in slabs:
            if income > limit:
                taxable = limit - previous_limit
            else:
                taxable = income - previous_limit

            if taxable > 0:
                tax += taxable * rate
                previous_limit = limit
            else:
                break

        return round(tax, 2)

    # ----------------------------
    # Surcharge
    # ----------------------------
    @staticmethod
    def _calculate_surcharge(base_tax, income):

        if income > 50000000:      # 5 Cr
            return round(base_tax * 0.37, 2)
        elif income > 20000000:    # 2 Cr
            return round(base_tax * 0.25, 2)
        elif income > 10000000:    # 1 Cr
            return round(base_tax * 0.15, 2)
        elif income > 5000000:     # 50 Lakh
            return round(base_tax * 0.10, 2)
        else:
            return 0.0

    # ----------------------------
    # Compare
    # ----------------------------
    @classmethod
    def compare_regimes(cls, gross_income, tax_year, deductions):

        if tax_year != "2025-26":
            raise ValueError("Only FY 2025-26 supported")

        # OLD REGIME
        old_taxable = max(gross_income - deductions, 0)
        old_base = cls._calculate_tax(old_taxable, cls.OLD_SLABS)
        old_surcharge = cls._calculate_surcharge(old_base, gross_income)
        old_cess = round((old_base + old_surcharge) * 0.04, 2)
        old_final = round(old_base + old_surcharge + old_cess, 2)

        # NEW REGIME
        new_taxable = gross_income
        new_base = cls._calculate_tax(new_taxable, cls.NEW_SLABS)
        new_surcharge = cls._calculate_surcharge(new_base, gross_income)
        new_cess = round((new_base + new_surcharge) * 0.04, 2)
        new_final = round(new_base + new_surcharge + new_cess, 2)

        if old_final < new_final:
            recommended = "old"
            savings = new_final - old_final
        elif new_final < old_final:
            recommended = "new"
            savings = old_final - new_final
        else:
            recommended = "same"
            savings = 0

        return {
            "tax_year": tax_year,
            "gross_income": gross_income,
            "old_regime": {
                "taxable_income": old_taxable,
                "final_tax": old_final
            },
            "new_regime": {
                "taxable_income": new_taxable,
                "final_tax": new_final
            },
            "recommended_regime": recommended,
            "tax_savings": round(savings, 2)
        }
