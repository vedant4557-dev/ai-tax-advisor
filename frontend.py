import streamlit as st
import requests

# ==============================
# CONFIG
# ==============================

BACKEND_URL = "https://ai-tax-advisor-1c0b.onrender.com/compare-regimes"
# If testing locally:
# BACKEND_URL = "http://127.0.0.1:8000/compare-regimes"

st.set_page_config(
    page_title="AI Tax Advisor",
    page_icon="💰",
    layout="centered"
)

# ==============================
# UI HEADER
# ==============================

st.title("💰 AI Tax Advisor")
st.caption("Compare Old vs New Tax Regime with AI-style explanation")

st.divider()

# ==============================
# INPUT SECTION
# ==============================

gross_income = st.number_input(
    "Enter your Gross Income (₹)",
    min_value=0.0,
    step=10000.0,
    format="%.2f"
)

tax_year = st.selectbox(
    "Select Tax Year",
    ["2024-25", "2025-26"]
)

deductions = st.number_input(
    "Deductions under Old Regime (₹)",
    min_value=0.0,
    step=10000.0,
    format="%.2f"
)

st.divider()

# ==============================
# ANALYZE BUTTON
# ==============================

if st.button("Analyze Tax"):

    if gross_income <= 0:
        st.error("Gross income must be greater than 0.")
        st.stop()

    payload = {
        "gross_income": gross_income,
        "tax_year": tax_year,
        "deductions": deductions
    }

    try:
        with st.spinner("Analyzing tax regimes..."):
            response = requests.post(BACKEND_URL, json=payload)

        if response.status_code != 200:
            st.error("Backend Error. Please check API.")
            st.write(response.text)
            st.stop()

        data = response.json()["data"]

        # ==============================
        # RESULTS SECTION
        # ==============================

        st.success(f"Recommended Regime: {data['recommended_regime'].upper()}")

        st.markdown("### 📊 Tax Comparison")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Old Regime Tax",
                f"₹{data['old_regime']['final_tax']:,.0f}"
            )

        with col2:
            st.metric(
                "New Regime Tax",
                f"₹{data['new_regime']['final_tax']:,.0f}"
            )

        st.metric(
            "Tax Savings",
            f"₹{data['tax_savings']:,.0f}"
        )

        st.divider()

        # ==============================
        # EFFECTIVE TAX RATE
        # ==============================

        st.markdown("### 📈 Effective Tax Rate")

        st.progress(min(int(data["effective_tax_rate_percent"]), 100))

        st.write(f"Effective Tax Rate: **{data['effective_tax_rate_percent']} %**")

        st.divider()

        # ==============================
        # AI EXPLANATION
        # ==============================

        st.markdown("### 🤖 AI Advisory Insight")

        st.info(data["ai_explanation"])

        st.divider()

        # ==============================
        # TAXABLE INCOME BREAKDOWN
        # ==============================

        st.markdown("### 🔎 Taxable Income Breakdown")

        col3, col4 = st.columns(2)

        with col3:
            st.write("Old Regime Taxable Income")
            st.code(f"₹{data['old_regime']['taxable_income']:,.0f}")

        with col4:
            st.write("New Regime Taxable Income")
            st.code(f"₹{data['new_regime']['taxable_income']:,.0f}")

    except Exception as e:
        st.error("Something went wrong while connecting to backend.")
        st.write(str(e))
