from domain.regime import TaxRegime
from domain.surcharge import Surcharge


class TaxCalculator:

    STANDARD_DEDUCTION = 50000
    CESS_RATE = 0.04

    @classmethod
    def compute_tax(
        cls,
        gross_income: float,
        regime: str,
        deductions: float = 0.0
    ) -> dict:

        # 1️⃣ Standard deduction
        taxable_income = gross_income - cls.STANDARD_DEDUCTION

        # 2️⃣ Apply deductions only for old regime
        if regime == "old":
            taxable_income -= deductions

        taxable_income = max(taxable_income, 0)

        # 3️⃣ Base tax from slabs
        if regime == "old":
            regime_result = TaxRegime.calculate_old(taxable_income)
            base_tax = regime_result["base_tax"]

        elif regime == "new":
            regime_result = TaxRegime.calculate_new(taxable_income)
            base_tax = regime_result["base_tax"]

        else:
            raise ValueError("Invalid regime. Choose 'old' or 'new'.")

        # 4️⃣ Surcharge
        surcharge = Surcharge.calculate_surcharge(base_tax, taxable_income)

        # 5️⃣ Cess (4%)
        cess = (base_tax + surcharge) * cls.CESS_RATE

        # 6️⃣ Final tax
        final_tax = base_tax + surcharge + cess

        # 7️⃣ Take home income
        take_home_income = gross_income - final_tax

        return {
    "regime": regime,
    "gross_income": gross_income,
    "taxable_income": taxable_income,
    "base_tax": round(base_tax, 2),
    "surcharge": round(surcharge, 2),
    "cess": round(cess, 2),
    "final_tax": round(base_tax + surcharge + cess, 2)
}
sec_80c = min(sec_80c, 150000)
nps_extra = min(nps_extra, 50000)
home_loan_interest = min(home_loan_interest, 200000)



