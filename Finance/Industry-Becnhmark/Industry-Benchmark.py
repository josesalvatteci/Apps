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
        st.write(f"🔄 Fetching data for {ticker_input}...")
        company = yf.Ticker(ticker_input)

        # Extract key financial data safely
        def get_financial_data(data_type):
            try:
                data = getattr(company, data_type)
                if data is not None and not data.empty:
                    return data.T  # Transpose for better readability
                else:
                    return pd.DataFrame({"Error": [f"No {data_type} data found"]})
            except Exception as e:
                return pd.DataFrame({"Error": [str(e)]})

        financials = get_financial_data("quarterly_financials")
        balance_sheet = get_financial_data("quarterly_balance_sheet")
        cashflow = get_financial_data("quarterly_cashflow")

        # Save to Excel
        excel_filename = f"{ticker_input}_financials.xlsx"
        with pd.ExcelWriter(excel_filename) as writer:
            financials.to_excel(writer, sheet_name="Financials")
            balance_sheet.to_excel(writer, sheet_name="Balance Sheet")
            cashflow.to_excel(writer, sheet_name="Cash Flow")

        # Display in Streamlit
        st.subheader(f"📜 {ticker_input} - Financials Overview")

        if not financials.empty:
            st.write("📊 **Income Statement**")
            st.dataframe(financials)
        else:
            st.warning("⚠️ No income statement data available.")

        if not balance_sheet.empty:
            st.write("🏦 **Balance Sheet**")
            st.dataframe(balance_sheet)
        else:
            st.warning("⚠️ No balance sheet data available.")

        if not cashflow.empty:
            st.write("💰 **Cash Flow Statement**")
            st.dataframe(cashflow)
        else:
            st.warning("⚠️ No cash flow data available.")

        # Download Button
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
