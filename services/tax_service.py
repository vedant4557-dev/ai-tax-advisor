# services/tax_service.py

from config.slabs_new import get_new_regime_slabs
from config.slabs_old import get_old_regime_slabs
from domain.surcharge import calculate_surcharge


class TaxService:

    @staticmethod
    def _calculate_tax_from_slabs(income: float, slabs):
        tax = 0
        previous_limit = 0

        for limit, rate in slabs:
            if income > limit:
                taxable_amount = limit - previous_limit
            else:
                taxable_amount = income - previous_limit

            if taxable_amount > 0:
                tax += taxable_amount * rate
                previous_limit = limit
            else:
                break

        return round(tax, 2)

    @staticmethod
    def _apply_cess(amount: float):
        return round(amount * 0.04, 2)

    @classmethod
    def _compute_regime(cls, regime: str, gross_income: float, tax_year: str, deductions: float):
        if regime == "old":
            slabs = get_old_regime_slabs(tax_year)
            taxable_income = max(gross_income - deductions, 0)
        else:
            slabs = get_new_regime_slabs(tax_year)
            taxable_income = gross_income

        base_tax = cls._calculate_tax_from_slabs(taxable_income, slabs)

        surcharge = calculate_surcharge(base_tax, gross_income)

        cess = cls._apply_cess(base_tax + surcharge)

        final_tax = round(base_tax + surcharge + cess, 2)

        return {
            "regime": regime,
            "gross_income": gross_income,
            "taxable_income": taxable_income,
            "base_tax": base_tax,
            "surcharge": surcharge,
            "cess": cess,
            "final_tax": final_tax,
        }

    @classmethod
    def compare_regimes(cls, gross_income: float, tax_year: str, deductions: float):

        old_result = cls._compute_regime(
            regime="old",
            gross_income=gross_income,
            tax_year=tax_year,
            deductions=deductions,
        )

        new_result = cls._compute_regime(
            regime="new",
            gross_income=gross_income,
            tax_year=tax_year,
            deductions=deductions,
        )

        if old_result["final_tax"] < new_result["final_tax"]:
            recommended = "old"
            savings = new_result["final_tax"] - old_result["final_tax"]
        elif new_result["final_tax"] < old_result["final_tax"]:
            recommended = "new"
            savings = old_result["final_tax"] - new_result["final_tax"]
        else:
            recommended = "same"
            savings = 0

        effective_rate = round(
            (min(old_result["final_tax"], new_result["final_tax"]) / gross_income) * 100,
            2,
        )

        return {
            "tax_year": tax_year,
            "gross_income": gross_income,
            "old_regime": old_result,
            "new_regime": new_result,
            "recommended_regime": recommended,
            "tax_savings": round(savings, 2),
            "effective_tax_rate_percent": effective_rate,
        }
