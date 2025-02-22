import streamlit as st
import pandas as pd
import os
from groq import Groq
from dotenv import load_dotenv

# Load API key securely
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("🚨 API Key is missing! Set it in Streamlit Secrets or a .env file.")
    st.stop()

# Streamlit Page Configuration
st.set_page_config(page_title="Chat with your Excel by Christian Martinez", page_icon="📊", layout="wide")
st.title("📊 Chat with your Excel by Christian Martinez")

# Upload Excel File
uploaded_file = st.file_uploader("📂 Upload your Excel file", type=["xls", "xlsx"])

def process_file(uploaded_file):
    """Reads the uploaded Excel file and returns a dictionary of DataFrames."""
    try:
        xls = pd.ExcelFile(uploaded_file)
        dataframes = {sheet: xls.parse(sheet) for sheet in xls.sheet_names}
        return dataframes
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return None

def summarize_data(df):
    """Generates a summary of the DataFrame to reduce data size before sending it to the AI."""
    summary = {
        "columns": list(df.columns),
        "num_rows": len(df),
        "num_columns": len(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "summary_stats": df.describe().to_dict()
    }
    return summary

if uploaded_file:
    sheets = process_file(uploaded_file)
    if sheets:
        sheet_name = st.selectbox("📑 Select a sheet to analyze", list(sheets.keys()))
        df = sheets[sheet_name]
        st.write("### Preview of Selected Sheet")
        st.dataframe(df)

        # Generate a summarized version of the data
        data_summary = summarize_data(df)

        # User Input for Question
        user_query = st.text_area("📝 Ask a question about the data")

        if st.button("🔍 Analyze with AI") and user_query:
            client = Groq(api_key=GROQ_API_KEY)
            prompt = f"""
            You are an AI data analyst. Below is a summary of the dataset:
            {data_summary}
            Based on this, answer the following question:
            {user_query}
            """

            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are an expert data analyst."},
                    {"role": "user", "content": prompt}
                ],
                model="llama3-8b-8192",
            )

            ai_response = response.choices[0].message.content
            
            # Display AI Response
            st.subheader("🤖 AI Response")
            st.write(ai_response)
    else:
        st.error("Failed to process the uploaded file. Please try again.")
