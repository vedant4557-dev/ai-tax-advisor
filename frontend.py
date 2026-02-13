import streamlit as st
import requests

st.set_page_config(page_title="AI Tax Advisor", page_icon="💰")

st.title("💰 AI Tax Advisor")
st.caption("Compare Old vs New Tax Regime with AI-style explanation")

gross_income = st.number_input("Enter your Gross Income (₹)", min_value=0.0, step=10000.0)
tax_year = st.selectbox("Select Tax Year", ["2024-25"])
deductions = st.number_input("Deductions under Old Regime (₹)", min_value=0.0, step=10000.0)

if st.button("Analyze Tax"):

    payload = {
        "gross_income": gross_income,
        "tax_year": tax_year,
        "deductions": deductions
    }

    response = requests.post(
        "http://127.0.0.1:8000/compare-regimes",
        json=payload
    )

    result = response.json()["data"]

    st.success(f"Recommended Regime: {result['recommended_regime'].upper()}")

    st.write("Old Regime Tax:", f"₹{result['old_regime']['final_tax']:,.0f}")
    st.write("New Regime Tax:", f"₹{result['new_regime']['final_tax']:,.0f}")
    st.write("Tax Savings:", f"₹{result['tax_savings']:,.0f}")

    st.markdown("---")
    st.subheader("AI Advisory Insight")
    st.write(result["ai_explanation"])


