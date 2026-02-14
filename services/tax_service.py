from typing import Dict, Any

from tax_engine.calculator import TaxCalculator
from services.ai_explanation_service import AIExplanationService


class TaxService:

    @staticmethod
    def compare_regimes(
        gross_income: float,
        tax_year: str,
        deductions: float = 0.0
    ) -> Dict[str, Any]:
        """
        Compares Old vs New tax regime and returns structured response
        with AI explanation.
        """

        # ---------------------------
        # Safety Validation
        # ---------------------------
        if gross_income is None or gross_income < 0:
            return {
                "error": "Invalid gross income provided."
            }

        try:
            # ---------------------------
            # Compute Old Regime
            # ---------------------------
            old_result = TaxCalculator.compute_tax(
                gross_income=gross_income,
                regime="old",
                deductions=deductions
            )

            # ---------------------------
            # Compute New Regime
            # ---------------------------
            new_result = TaxCalculator.compute_tax(
                gross_income=gross_income,
                regime="new",
                deductions=0
            )

            old_tax = float(old_result.get("final_tax", 0))
            new_tax = float(new_result.get("final_tax", 0))

            # ---------------------------
            # Compare Regimes
            # ---------------------------
            if old_tax < new_tax:
                recommended = "old"
                savings = new_tax - old_tax
            elif new_tax < old_tax:
                recommended = "new"
                savings = old_tax - new_tax
            else:
                recommended = "same"
                savings = 0.0

            # ---------------------------
            # Effective Tax Rate
            # ---------------------------
            effective_tax_rate = (
                (min(old_tax, new_tax) / gross_income) * 100
                if gross_income > 0 else 0
            )

            # ---------------------------
            # Final Structured Result
            # ---------------------------
            result = {
                "tax_year": tax_year,
                "gross_income": gross_income,
                "old_regime": old_result,
                "new_regime": new_result,
                "recommended_regime": recommended,
                "tax_savings": round(savings, 2),
                "effective_tax_rate_percent": round(effective_tax_rate, 2)
            }

            # ---------------------------
            # AI Explanation Layer
            # ---------------------------
            result["ai_explanation"] = (
                AIExplanationService.generate_explanation(result)
            )

            return result

        except Exception as e:
            return {
                "error": f"Tax comparison failed: {str(e)}"
            }
