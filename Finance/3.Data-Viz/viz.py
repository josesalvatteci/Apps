import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from groq import Groq
from dotenv import load_dotenv

# Load API key securely
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("🚨 API Key is missing! Set it in Streamlit Secrets or a .env file.")
    st.stop()

# Streamlit UI for file upload
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("Data Preview:", df.head())
    
    # Create a sample prompt for the LLM
    data_sample = df.head().to_json()
    user_request = st.text_input("Describe your visualization (e.g., 'bar chart of sales'):")
    
    if user_request:
        prompt = f"""
        Using the following data sample: {data_sample},
        generate Python code that creates a {user_request} using matplotlib or seaborn.
        """
        # Call Groq API
        client = Groq(api_key=GROQ_API_KEY)
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a Python data visualization expert."},
                {"role": "user", "content": prompt}
            ],
            model="llama3-8b-8192",
        )
        generated_code = response.choices[0].message.content
        
        st.subheader("Generated Code")
        st.code(generated_code, language="python")
        
        # Execute the generated code safely
        try:
            # Define a safe execution context
            exec_globals = {
                "df": df, 
                "pd": pd, 
                "plt": plt, 
                "st": st
            }
            exec(generated_code, exec_globals)
        except Exception as e:
            st.error(f"Error executing generated code: {e}")
