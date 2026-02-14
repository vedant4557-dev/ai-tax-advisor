import streamlit as st
import requests

BACKEND_URL = "https://ai-tax-advisor-1c0b.onrender.com/compare-regimes"


st.set_page_config(page_title="AI Tax Advisor", layout="centered")

st.title("💰 AI Tax Advisor")
st.markdown("Salary-based Old vs New Tax Regime Comparison")

# ---------------------------
# Salary Structure
# ---------------------------
st.header("🧾 Salary Structure")

basic_salary = st.number_input("Basic Salary (₹)", min_value=0.0)
hra_received = st.number_input("HRA Received (₹)", min_value=0.0)
special_allowance = st.number_input("Special Allowance (₹)", min_value=0.0)
other_income = st.number_input("Other Income (₹)", min_value=0.0)

# ---------------------------
# Deductions (Old Regime)
# ---------------------------
st.header("📉 Deductions (Old Regime Only)")

sec_80c = st.number_input("Section 80C (Max ₹1,50,000)", min_value=0.0)
sec_80d = st.number_input("Section 80D (Health Insurance)", min_value=0.0)
home_loan_interest = st.number_input("Home Loan Interest (Max ₹2L)", min_value=0.0)
nps_extra = st.number_input("NPS 80CCD(1B) (Max ₹50,000)", min_value=0.0)

tax_year = st.selectbox("Select Tax Year", ["2024-25"])

# ---------------------------
# Compute Total Income
# ---------------------------
gross_income = (
    basic_salary +
    hra_received +
    special_allowance +
    other_income
)

total_deductions = (
    min(sec_80c, 150000) +
    sec_80d +
    min(home_loan_interest, 200000) +
    min(nps_extra, 50000)
)

# ---------------------------
# Call Backend
# ---------------------------
if st.button("Analyze Tax"):

    payload = {
        "gross_income": gross_income,
        "tax_year": tax_year,
        "deductions": total_deductions
    }

    try:
        response = requests.post(BACKEND_URL, json=payload)

        # Check HTTP status
        if response.status_code != 200:
            st.error(f"Backend error: {response.status_code}")
            st.stop()

        response_json = response.json()

        # Check backend status field
        if response_json.get("status") != "success":
            st.error("Backend returned error response.")
            st.stop()

        result = response_json["data"]

        # ===============================
        # ✅ Display Results
        # ===============================

        st.success(
            f"Recommended Regime: {result['recommended_regime'].upper()}"
        )

        st.markdown("### 📊 Tax Comparison")

        st.write(
            f"Old Regime Tax: ₹{result['old_regime']['final_tax']:,.0f}"
        )
        st.write(
            f"New Regime Tax: ₹{result['new_regime']['final_tax']:,.0f}"
        )
        st.write(
            f"Tax Savings: ₹{result['tax_savings']:,.0f}"
        )
        st.write(
            f"Effective Tax Rate: {result['effective_tax_rate_percent']}%"
        )

        st.markdown("### 🤖 AI Advisory Insight")
        st.write(result["ai_explanation"])

    except Exception as e:
        st.error("Error connecting to backend.")
        st.write(str(e))
