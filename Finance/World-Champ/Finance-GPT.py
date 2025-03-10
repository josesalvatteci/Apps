import streamlit as st
import pandas as pd
import numpy as np
import matplotlib as plt
from fbprophet import Prophet
import os
from dotenv import load_dotenv

# Load API Key (Optional for Future Enhancements)
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Streamlit UI Styling
st.set_page_config(page_title="Finance GPT - The World Champion Forecaster", page_icon="📈", layout="wide")
st.title("🏆 Finance GPT - The World Champion Forecaster")
st.write("Upload your financial data and let AI predict the future!")

# File Upload Section
uploaded_file = st.file_uploader("Upload an Excel file with a Date column", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("### Preview of Uploaded Data")
    st.dataframe(df.head())

    # Ensure Date Column is in Datetime Format
    date_col = st.selectbox("Select the Date Column", df.columns)
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

    # Select the Column to Forecast
    forecast_col = st.selectbox("Select the Column to Forecast", [col for col in df.columns if col != date_col])

    # Prepare Data for Prophet
    data = df[[date_col, forecast_col]].rename(columns={date_col: "ds", forecast_col: "y"})

    # Forecasting with Prophet
    st.write("### Forecasting in Progress...")
    model = Prophet()
    model.fit(data)
    
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)

    # Plot Forecast
    st.write("### Forecast Results")
    fig1 = model.plot(forecast)
    st.pyplot(fig1)
    
    # Download Forecast Results
    forecast_download = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]
    forecast_download.columns = ["Date", "Forecast", "Lower Bound", "Upper Bound"]
    forecast_file = "forecast_results.xlsx"
    forecast_download.to_excel(forecast_file, index=False)
    
    with open(forecast_file, "rb") as file:
        st.download_button(label="📥 Download Forecast Results", data=file, file_name=forecast_file, mime="application/vnd.ms-excel")

    st.success("🎉 Forecasting Complete! Download your results above.")
