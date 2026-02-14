from domain.slabs_old import calculate_old_regime_tax
from domain.slabs_new import calculate_new_regime_tax
from domain.surcharge import calculate_surcharge

STANDARD_DEDUCTION = 50000
CESS_RATE = 0.04


class TaxService:

    @staticmethod
    def calculate_hra_exemption(basic_salary, hra_received, annual_rent_paid, metro_city):
        if annual_rent_paid == 0:
            return 0

        rent_minus_10_percent = max(0, annual_rent_paid - (0.10 * basic_salary))
        percent_salary = 0.50 * basic_salary if metro_city else 0.40 * basic_salary

        return min(hra_received, rent_minus_10_percent, percent_salary)

    @staticmethod
    def apply_deduction_limits(section_80c, section_80d, home_loan_interest, nps_80ccd1b):
        capped_80c = min(section_80c, 150000)
        capped_80d = min(section_80d, 50000)
        capped_home_loan = min(home_loan_interest, 200000)
        capped_nps = min(nps_80ccd1b, 50000)

        return capped_80c + capped_80d + capped_home_loan + capped_nps

    @staticmethod
    def compute_final_tax(base_tax, gross_income):
        surcharge = calculate_surcharge(base_tax, gross_income)
        cess = (base_tax + surcharge) * CESS_RATE
        final_tax = base_tax + surcharge + cess

        return {
            "base_tax": round(base_tax, 2),
            "surcharge": round(surcharge, 2),
            "cess": round(cess, 2),
            "final_tax": round(final_tax, 2)
        }

    @staticmethod
    def generate_ai_explanation(gross_income, recommended_regime, tax_savings):
        if recommended_regime == "same":
            return (
                f"For a gross income of ₹{gross_income:,.0f}, both tax regimes result in the same liability. "
                "Your choice should depend on expected future deductions or long-term tax planning strategy."
            )

        if recommended_regime == "old":
            return (
                f"With a gross income of ₹{gross_income:,.0f}, the Old Tax Regime provides better tax efficiency. "
                f"You save ₹{tax_savings:,.0f} compared to the New Regime. "
                "This typically benefits individuals actively claiming deductions like 80C, 80D or home loan interest."
            )

        return (
            f"For a gross income of ₹{gross_income:,.0f}, the New Tax Regime results in lower tax liability. "
            f"You save ₹{tax_savings:,.0f} compared to the Old Regime. "
            "This regime works well if you prefer simplified taxation without investment-linked deductions."
        )

    @staticmethod
    def compare_regimes(
        basic_salary,
        hra_received,
        special_allowance,
        other_income,
        annual_rent_paid,
        metro_city,
        section_80c,
        section_80d,
        home_loan_interest,
        nps_80ccd1b,
        tax_year
    ):

        # =========================
        # 1. Gross Income
        # =========================
        gross_income = (
            basic_salary +
            hra_received +
            special_allowance +
            other_income
        )

        # =========================
        # 2. HRA Exemption (Old Only)
        # =========================
        hra_exemption = TaxService.calculate_hra_exemption(
            basic_salary,
            hra_received,
            annual_rent_paid,
            metro_city
        )

        # =========================
        # 3. Old Regime Calculation
        # =========================
        total_deductions = TaxService.apply_deduction_limits(
            section_80c,
            section_80d,
            home_loan_interest,
            nps_80ccd1b
        )

        taxable_income_old = max(
            0,
            gross_income
            - hra_exemption
            - STANDARD_DEDUCTION
            - total_deductions
        )

        base_tax_old = calculate_old_regime_tax(taxable_income_old)
        old_regime_tax = TaxService.compute_final_tax(base_tax_old, gross_income)

        # =========================
        # 4. New Regime Calculation
        # =========================
        taxable_income_new = max(
            0,
            gross_income - STANDARD_DEDUCTION
        )

        base_tax_new = calculate_new_regime_tax(taxable_income_new)
        new_regime_tax = TaxService.compute_final_tax(base_tax_new, gross_income)

        # =========================
        # 5. Comparison
        # =========================
        old_final = old_regime_tax["final_tax"]
        new_final = new_regime_tax["final_tax"]

        if old_final < new_final:
            recommended = "old"
            savings = new_final - old_final
        elif new_final < old_final:
            recommended = "new"
            savings = old_final - new_final
        else:
            recommended = "same"
            savings = 0

        effective_tax_rate = (min(old_final, new_final) / gross_income) * 100 if gross_income > 0 else 0

        ai_explanation = TaxService.generate_ai_explanation(
            gross_income,
            recommended,
            savings
        )

        # =========================
        # 6. Final Structured Response
        # =========================
        return {
            "tax_year": tax_year,
            "gross_income": round(gross_income, 2),
            "hra_exemption": round(hra_exemption, 2),
            "standard_deduction": STANDARD_DEDUCTION,
            "total_deductions": round(total_deductions, 2),
            "old_regime": {
                "regime": "old",
                "taxable_income": round(taxable_income_old, 2),
                **old_regime_tax
            },
            "new_regime": {
                "regime": "new",
                "taxable_income": round(taxable_income_new, 2),
                **new_regime_tax
            },
            "recommended_regime": recommended,
            "tax_savings": round(savings, 2),
            "effective_tax_rate_percent": round(effective_tax_rate, 2),
            "ai_explanation": ai_explanation
        }
