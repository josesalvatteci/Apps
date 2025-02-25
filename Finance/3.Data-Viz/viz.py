import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from groq import Groq
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("🚨 API Key is missing! Set it in Streamlit Secrets or a .env file.")
    st.stop()

st.set_page_config(page_title="AI Code Generator", page_icon="📊", layout="wide")

# UI
st.subheader("📤 Upload Excel File and Enter Your Request")
uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])
user_prompt = st.text_input("What would you like to do? (e.g., 'Create a bar chart of total sales by category')")

if uploaded_file and user_prompt:
    # Read Excel file
    df = pd.read_excel(uploaded_file)
    st.write("Data Preview:", df.head())

    # Prepare prompt
    columns = df.columns.tolist()
    columns_str = ", ".join(columns)
    ai_prompt = f"""
    Write a Python function named create_plot that takes a pandas DataFrame df as input and returns a matplotlib figure.
    The DataFrame has the following columns: {columns_str}.
    The function should create a bar chart based on the following request: '{user_prompt}'.
    Use only the matplotlib.pyplot and pandas libraries, and do not include any code outside the function definition.
    """

    # Call Groq API
    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an expert Python programmer specializing in data visualization."},
            {"role": "user", "content": ai_prompt}
        ],
        model="llama3-8b-8192",
    )
    generated_code = response.choices[0].message.content.strip()
    st.subheader("Generated Code")
    st.code(generated_code, language="python")

    # Execute the code
    globals_dict = {"pd": pd, "plt": plt, "df": df}
    try:
        exec(generated_code, globals_dict)
        fig = globals_dict["create_plot"](df)
        st.subheader("Generated Visualization")
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error executing the generated code: {str(e)}")
