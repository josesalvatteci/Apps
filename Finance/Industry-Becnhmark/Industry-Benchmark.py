import streamlit as st
import pandas as pd
import yfinance as yf
import os
import matplotlib.pyplot as plt
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

# **💡 User Input for Tickers**
tickers = st.text_input("Enter company ticker symbols separated by commas (e.g., AAPL, MSFT, TSLA):")

if tickers:
    ticker_list = [ticker.strip().upper() for ticker in tickers.split(",")]

    all_data = {}

    for ticker in ticker_list:
        try:
            st.write(f"🔄 Fetching data for {ticker}...")
            company = yf.Ticker(ticker)

            # Function to safely fetch data
            def get_financial_data(data_type):
                try:
                    data = getattr(company, data_type)
                    if data is not None and not data.empty:
                        return data.T  # Transpose for better readability
                    else:
                        return pd.DataFrame({f"No {data_type} data": []})
                except Exception as e:
                    return pd.DataFrame({f"Error fetching {data_type}": [str(e)]})

            # Fetch financials
            financials = get_financial_data("quarterly_financials")
            balance_sheet = get_financial_data("quarterly_balance_sheet")
            cashflow = get_financial_data("quarterly_cashflow")

            # Save Data
            all_data[ticker] = {
                "financials": financials,
                "balance_sheet": balance_sheet,
                "cashflow": cashflow,
            }

        except Exception as e:
            st.error(f"⚠️ Error fetching data for {ticker}: {str(e)}")

    # **📈 Multi-Company Graph Selection**
    st.subheader("📊 Compare Metrics Across Companies")

    # Available financial metrics
    available_metrics = set()
    for ticker in all_data:
        available_metrics.update(all_data[ticker]["financials"].columns)

    selected_metrics = st.multiselect("Select financial metrics to compare", list(available_metrics), default=["Total Revenue"])

    if selected_metrics:
        fig, ax = plt.subplots(figsize=(12, 6))
        
        for ticker in ticker_list:
            if ticker in all_data:
                financials = all_data[ticker]["financials"]
                for metric in selected_metrics:
                    if metric in financials.columns:
                        ax.plot(financials.index, financials[metric], marker='o', label=f"{ticker} - {metric}")

        ax.set_title("Financial Metrics Comparison")
        ax.set_xlabel("Quarter")
        ax.set_ylabel("Value")
        ax.legend()
        ax.grid(True)
        
        # Show graph
        st.pyplot(fig)

    # **📥 Download All Data as Excel**
    if all_data:
        excel_filename = "financial_data_comparison.xlsx"
        with pd.ExcelWriter(excel_filename) as writer:
            for ticker in all_data:
                all_data[ticker]["financials"].to_excel(writer, sheet_name=f"{ticker}_Financials")
                all_data[ticker]["balance_sheet"].to_excel(writer, sheet_name=f"{ticker}_BalanceSheet")
                all_data[ticker]["cashflow"].to_excel(writer, sheet_name=f"{ticker}_CashFlow")

        st.download_button(
            label="📥 Download All Financial Data (Excel)",
            data=open(excel_filename, "rb").read(),
            file_name=excel_filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # **🔍 AI Analysis for the First Company Only**
    st.subheader("🧠 AI-Powered Industry & Company Analysis")

    if ticker_list:
        first_ticker = ticker_list[0]
        company = yf.Ticker(first_ticker)

        # Define AI Prompt
        prompt = f"""
        You are a financial analyst. Provide a detailed analysis of {first_ticker}, including:
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
