import streamlit as st
import pandas as pd
import yfinance as yf
import os
from groq import Groq
from dotenv import load_dotenv

# **🔒 Load API Key Securely**
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("🚨 API Key is missing! Set it in Streamlit Secrets or a .env file.")
    st.stop()

# **📊 Streamlit UI**
st.set_page_config(page_title="AI Financial Analysis", page_icon="📈", layout="wide")
st.title("📊 AI-Powered Financial Analysis")

# **💡 User Input for Ticker Symbol**
ticker_input = st.text_input("Enter a company ticker symbol (e.g., AAPL, MSFT, TSLA):")

if ticker_input:
    try:
        # Fetch financial data
        st.write(f"Fetching data for {ticker_input}...")
        company = yf.Ticker(ticker_input)

        # Extract key financial data
        financials = company.quarterly_financials.T
        balance_sheet = company.quarterly_balance_sheet.T
        cashflow = company.quarterly_cashflow.T

        # Save to Excel
        excel_filename = f"{ticker_input}_financials.xlsx"
        with pd.ExcelWriter(excel_filename) as writer:
            financials.to_excel(writer, sheet_name="Financials")
            balance_sheet.to_excel(writer, sheet_name="Balance Sheet")
            cashflow.to_excel(writer, sheet_name="Cash Flow")

        # Display in Streamlit
        st.subheader(f"📜 {ticker_input} - Financials Overview")
        st.write(financials)
        st.download_button(
            label="📥 Download Financial Data (Excel)",
            data=open(excel_filename, "rb").read(),
            file_name=excel_filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # **🔍 AI Analysis**
        st.subheader("🧠 AI-Powered Industry & Company Analysis")

        # Define AI Prompt
        prompt = f"""
        You are a financial analyst. Provide a detailed analysis of {ticker_input}, including:
        - Key financial trends.
        - Industry comparison.
        - Areas of concern or opportunity.
        - Actionable insights for investors.

        Company Data:
        - Business Summary: {company.info.get('longBusinessSummary', 'N/A')}
        - Sector: {company.info.get('sector', 'N/A')}
        - Industry: {company.info.get('industry', 'N/A')}
        """

        # Call Groq API for AI-generated insights
        client = Groq(api_key=GROQ_API_KEY)
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a financial expert providing stock analysis."},
                {"role": "user", "content": prompt}
            ],
            model="llama3-8b-8192",
        )

        # Display AI response
        ai_commentary = response.choices[0].message.content
        st.write(ai_commentary)

    except Exception as e:
        st.error(f"⚠️ Error fetching data: {str(e)}")
