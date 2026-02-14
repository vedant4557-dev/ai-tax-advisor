from config.slabs_old import OLD_REGIME_SLABS
from config.slabs_new import NEW_REGIME_SLABS
from domain.surcharge import calculate_surcharge
from domain.rebate import calculate_rebate


CESS_RATE = 0.04
STANDARD_DEDUCTION = 50000


class TaxService:

    @staticmethod
    def _calculate_tax_from_slabs(income: float, slabs: list) -> float:
        tax = 0
        remaining_income = income

        for lower, upper, rate in slabs:
            if remaining_income <= 0:
                break

            if upper is None:
                taxable_amount = remaining_income
            else:
                taxable_amount = min(remaining_income, upper - lower)

            tax += taxable_amount * rate
            remaining_income -= taxable_amount

        return tax

    @staticmethod
    def _build_regime_response(
        regime_name: str,
        gross_income: float,
        taxable_income: float,
        base_tax: float
    ) -> dict:

        surcharge = calculate_surcharge(taxable_income, base_tax)
        cess = (base_tax + surcharge) * CESS_RATE
        final_tax = base_tax + surcharge + cess

        return {
            "regime": regime_name,
            "gross_income": gross_income,
            "taxable_income": taxable_income,
            "base_tax": round(base_tax, 2),
            "surcharge": round(surcharge, 2),
            "cess": round(cess, 2),
            "final_tax": round(final_tax, 2),
        }

    @staticmethod
    def compare_regimes(
        gross_income: float,
        tax_year: str,
        deductions: float = 0
    ) -> dict:

        # OLD REGIME
        taxable_old = max(
            gross_income - STANDARD_DEDUCTION - deductions,
            0
        )

        base_tax_old = TaxService._calculate_tax_from_slabs(
            taxable_old,
            OLD_REGIME_SLABS
        )

        rebate_old = calculate_rebate(taxable_old, base_tax_old)
        base_tax_old -= rebate_old

        old_regime = TaxService._build_regime_response(
            "old",
            gross_income,
            taxable_old,
            base_tax_old
        )

        # NEW REGIME
        taxable_new = max(gross_income - STANDARD_DEDUCTION, 0)

        base_tax_new = TaxService._calculate_tax_from_slabs(
            taxable_new,
            NEW_REGIME_SLABS
        )

        rebate_new = calculate_rebate(taxable_new, base_tax_new)
        base_tax_new -= rebate_new

        new_regime = TaxService._build_regime_response(
            "new",
            gross_income,
            taxable_new,
            base_tax_new
        )

        # Comparison
        tax_savings = abs(old_regime["final_tax"] - new_regime["final_tax"])

        if old_regime["final_tax"] < new_regime["final_tax"]:
            recommended = "old"
        elif new_regime["final_tax"] < old_regime["final_tax"]:
            recommended = "new"
        else:
            recommended = "same"

        effective_tax_rate = (
            (min(old_regime["final_tax"], new_regime["final_tax"]) / gross_income) * 100
            if gross_income > 0 else 0
        )

        return {
            "tax_year": tax_year,
            "gross_income": gross_income,
            "old_regime": old_regime,
            "new_regime": new_regime,
            "recommended_regime": recommended,
            "tax_savings": round(tax_savings, 2),
            "effective_tax_rate_percent": round(effective_tax_rate, 2),
        }
