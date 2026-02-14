import streamlit as st
import requests

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="AI Tax Advisor", page_icon="💰")

st.title("💰 AI Tax Advisor")
st.caption("Salary-based Old vs New Tax Regime Comparison with Smart Deduction Logic")

# =============================
# SALARY STRUCTURE
# =============================

st.subheader("🧾 Salary Structure")

basic_salary = st.number_input("Basic Salary (₹)", min_value=0.0)
hra_received = st.number_input("HRA Received (₹)", min_value=0.0)
special_allowance = st.number_input("Special Allowance (₹)", min_value=0.0)
other_income = st.number_input("Other Income (₹)", min_value=0.0)

rent_paid = st.number_input("Annual Rent Paid (₹)", min_value=0.0)
metro_city = st.checkbox("Living in Metro City?")

# =============================
# HRA EXEMPTION CALCULATION
# =============================

if metro_city:
    hra_limit = 0.5 * basic_salary
else:
    hra_limit = 0.4 * basic_salary

rent_minus_10_percent = rent_paid - (0.1 * basic_salary)

hra_exemption = min(
    hra_received,
    hra_limit,
    rent_minus_10_percent if rent_minus_10_percent > 0 else 0
)

# =============================
# GROSS INCOME
# =============================

gross_income = (
    basic_salary +
    hra_received +
    special_allowance +
    other_income
)

standard_deduction = 50000

# =============================
# DEDUCTIONS (OLD REGIME)
# =============================

st.subheader("📉 Deductions (Old Regime Only)")

sec_80c = st.number_input("Section 80C (Max ₹1,50,000)", min_value=0.0, max_value=150000.0)
sec_80d = st.number_input("Section 80D (Health Insurance)", min_value=0.0)
home_loan_interest = st.number_input("Home Loan Interest (Section 24, Max ₹2L)", min_value=0.0, max_value=200000.0)
nps_extra = st.number_input("NPS 80CCD(1B) (Max ₹50,000)", min_value=0.0, max_value=50000.0)

total_deductions = sec_80c + sec_80d + home_loan_interest + nps_extra

tax_year = st.selectbox("Select Tax Year", ["2024-25"])

# =============================
# ANALYZE BUTTON
# =============================

if st.button("Analyze Tax"):

    payload = {
        "gross_income": gross_income,
        "tax_year": tax_year,
        "deductions": total_deductions + hra_exemption + standard_deduction
    }

    response = requests.post(
        "https://ai-tax-advisor-1c0b.onrender.com/compare-regimes",
        json=payload
    )

    result = response.json()["data"]

    st.success(f"Recommended Regime: {result['recommended_regime'].upper()}")

    st.markdown("---")

    st.subheader("📊 Tax Comparison")

    st.write("Gross Income:", f"₹{gross_income:,.0f}")
    st.write("HRA Exemption:", f"₹{hra_exemption:,.0f}")
    st.write("Standard Deduction:", f"₹{standard_deduction:,.0f}")
    st.write("Other Deductions:", f"₹{total_deductions:,.0f}")

    st.markdown("---")

    st.write("Old Regime Tax:", f"₹{result['old_regime']['final_tax']:,.0f}")
    st.write("New Regime Tax:", f"₹{result['new_regime']['final_tax']:,.0f}")
    st.write("Tax Savings:", f"₹{result['tax_savings']:,.0f}")

    st.markdown("---")
    st.subheader("🤖 AI Advisory Insight")
    st.write(result["ai_explanation"])


