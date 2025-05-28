import streamlit as st
import requests

st.set_page_config(page_title="Currency Converter", layout="centered")

st.title("Currency Converter")

# Supported currencies (subset of popular currencies)
currency_symbols = {
    "USD": "United States Dollar",
    "EUR": "Euro",
    "GBP": "British Pound Sterling",
    "JPY": "Japanese Yen",
    "AUD": "Australian Dollar",
    "CAD": "Canadian Dollar",
    "CHF": "Swiss Franc",
    "CNY": "Chinese Yuan",
    "INR": "Indian Rupee",
    "BRL": "Brazilian Real"
}

amount = st.number_input("Enter amount to convert", min_value=0.0, format="%.2f", value=1.0)

col1, col2 = st.columns(2)
with col1:
    from_currency = st.selectbox("From", options=list(currency_symbols.keys()), format_func=lambda x: f"{x} - {currency_symbols[x]}")
with col2:
    to_currency = st.selectbox("To", options=list(currency_symbols.keys()), index=1, format_func=lambda x: f"{x} - {currency_symbols[x]}")

def get_exchange_rate(base: str, target: str):
    url = f"https://api.exchangerate.host/latest?base={base}&symbols={target}"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("success", True):
            rate = data["rates"][target]
            return rate
        else:
            st.error("Failed to fetch exchange rates.")
            return None
    except Exception as e:
        st.error(f"Error fetching exchange rates: {e}")
        return None

if st.button("Convert"):
    if from_currency == to_currency:
        st.write(f"{amount:.2f} {from_currency} = {amount:.2f} {to_currency}")
    else:
        rate = get_exchange_rate(from_currency, to_currency)
        if rate is not None:
            converted_amount = amount * rate
            st.success(f"{amount:.2f} {from_currency} = {converted_amount:.2f} {to_currency}")

