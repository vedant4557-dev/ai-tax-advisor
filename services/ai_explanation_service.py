class AIExplanationService:

    @staticmethod
    def generate_explanation(result: dict) -> str:

        income = result["gross_income"]
        old_tax = result["old_regime"]["final_tax"]
        new_tax = result["new_regime"]["final_tax"]
        savings = result["tax_savings"]
        recommended = result["recommended_regime"]
        rate = result["effective_tax_rate_percent"]

        # Income classification
        if income < 700000:
            income_segment = "lower income bracket"
        elif income < 1500000:
            income_segment = "middle income bracket"
        else:
            income_segment = "high income bracket"

        # Regime logic
        if recommended == "same":
            return (
                f"For a gross income of ₹{income:,.0f}, both tax regimes result in the same liability. "
                f"You fall under the {income_segment}. In such cases, your decision should depend on "
                f"future deductions or expected investments rather than immediate tax savings."
            )

        if recommended == "new":

            advisory = (
                "The New Tax Regime is generally more beneficial for individuals who "
                "do not claim significant deductions such as 80C, HRA, or housing loan interest."
            )

            return (
                f"With a gross income of ₹{income:,.0f}, you fall under the {income_segment}. "
                f"The New Tax Regime results in a lower tax liability of ₹{new_tax:,.0f}, "
                f"saving you ₹{savings:,.0f} compared to the Old Regime. "
                f"Your effective tax rate stands at {rate}%. "
                f"{advisory} "
                f"This regime offers simplicity and lower compliance burden."
            )

        # If Old regime better
        advisory = (
            "The Old Tax Regime typically benefits taxpayers who actively invest "
            "in tax-saving instruments or claim housing loan benefits."
        )

        return (
            f"With a gross income of ₹{income:,.0f}, you fall under the {income_segment}. "
            f"The Old Tax Regime results in a lower tax liability of ₹{old_tax:,.0f}, "
            f"saving you ₹{savings:,.0f} compared to the New Regime. "
            f"Your effective tax rate stands at {rate}%. "
            f"{advisory} "
            f"Strategic tax planning under this regime can further optimize savings."
        )

