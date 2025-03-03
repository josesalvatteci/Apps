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
st.set_page_config(page_title="AI Financial Benchmarking Tool", page_icon="📈", layout="wide")
st.title("📊 AI Financial Benchmarking Tool")

# **💡 User Selection: Single or Multi-Company Analysis**
analysis_type = st.radio("Select Analysis Type:", ["Single Company Analysis", "Multi-Company Comparison"])

if analysis_type == "Single Company Analysis":
    # **📌 Single Company Analysis**
    ticker = st.text_input("Enter a company ticker symbol (e.g., AAPL, MSFT, TSLA):")

    if ticker:
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

            # Display Data
            st.subheader(f"📜 {ticker} - Financial Statements")
            st.write("📊 **Income Statement**")
            st.dataframe(financials)

            st.write("🏦 **Balance Sheet**")
            st.dataframe(balance_sheet)

            st.write("💰 **Cash Flow Statement**")
            st.dataframe(cashflow)

            # Save to Excel
            excel_filename = f"{ticker}_financials.xlsx"
            with pd.ExcelWriter(excel_filename) as writer:
                financials.to_excel(writer, sheet_name="Financials")
                balance_sheet.to_excel(writer, sheet_name="Balance Sheet")
                cashflow.to_excel(writer, sheet_name="Cash Flow")

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
            You are a financial analyst. Provide a detailed analysis of {ticker}, including:
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

elif analysis_type == "Multi-Company Comparison":
    # **📌 Multi-Company Comparison**
    tickers = st.text_input("Enter multiple company ticker symbols (comma-separated, e.g., AAPL, MSFT, TSLA):")

    if tickers:
        ticker_list = [ticker.strip().upper() for ticker in tickers.split(",")]
        all_data = {}

        for ticker in ticker_list:
            try:
                st.write(f"🔄 Fetching data for {ticker}...")
                company = yf.Ticker(ticker)

                # Fetch financials safely
                def get_financial_data(data_type):
                    try:
                        data = getattr(company, data_type)
                        if data is not None and not data.empty:
                            return data.T  # Transpose for better readability
                        else:
                            return pd.DataFrame({f"No {data_type} data": []})
                    except Exception as e:
                        return pd.DataFrame({f"Error fetching {data_type}": [str(e)]})

                # Store data
                all_data[ticker] = {
                    "financials": get_financial_data("quarterly_financials"),
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

            st.download_button(
                label="📥 Download All Financial Data (Excel)",
                data=open(excel_filename, "rb").read(),
                file_name=excel_filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
