class TaxRegime:
    """
    Handles tax calculations for Old and New Indian tax regimes.
    Returns structured output compatible with TaxCalculator.
    """

    CESS_RATE = 0.04  # 4% Health & Education Cess

    # ============================================
    # OLD REGIME
    # ============================================

    @classmethod
    def calculate_old(cls, taxable_income: float) -> dict:
        """
        Calculates tax under Old Regime.
        """

        base_tax = cls._calculate_old_slabs(taxable_income)

        # Rebate under 87A (Old Regime)
        if taxable_income <= 500000:
            base_tax = 0

        cess = base_tax * cls.CESS_RATE
        final_tax = base_tax + cess

        return {
            "base_tax": round(base_tax, 2),
            "cess": round(cess, 2),
            "final_tax": round(final_tax, 2)
        }

    # ============================================
    # NEW REGIME
    # ============================================

    @classmethod
    def calculate_new(cls, taxable_income: float) -> dict:
        """
        Calculates tax under New Regime (latest slabs).
        """

        base_tax = cls._calculate_new_slabs(taxable_income)

        # Rebate under 87A (New Regime - up to 7L)
        if taxable_income <= 700000:
            base_tax = 0

        cess = base_tax * cls.CESS_RATE
        final_tax = base_tax + cess

        return {
            "base_tax": round(base_tax, 2),
            "cess": round(cess, 2),
            "final_tax": round(final_tax, 2)
        }

    # ============================================
    # OLD SLAB CALCULATION
    # ============================================

    @staticmethod
    def _calculate_old_slabs(income: float) -> float:
        tax = 0

        if income <= 250000:
            return 0

        if income > 250000:
            tax += min(income - 250000, 250000) * 0.05

        if income > 500000:
            tax += min(income - 500000, 500000) * 0.20

        if income > 1000000:
            tax += (income - 1000000) * 0.30

        return tax

    # ============================================
    # NEW SLAB CALCULATION
    # ============================================

    @staticmethod
    def _calculate_new_slabs(income: float) -> float:
        tax = 0

        slabs = [
            (300000, 0.00),
            (300000, 0.05),
            (300000, 0.10),
            (300000, 0.15),
            (300000, 0.20),
            (float("inf"), 0.30),
        ]

        remaining_income = income

        for slab_amount, rate in slabs:
            taxable_amount = min(remaining_income, slab_amount)
            tax += taxable_amount * rate
            remaining_income -= taxable_amount

            if remaining_income <= 0:
                break

        return tax

