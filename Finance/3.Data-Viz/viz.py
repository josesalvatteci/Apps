import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from groq import Groq
from dotenv import load_dotenv

# Load API key securely
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("🚨 API Key is missing! Set it in Streamlit Secrets or a .env file.")
    st.stop()

# 🎨 Streamlit UI Styling
st.set_page_config(page_title="FP&A AI Learning Advisor", page_icon="🤖", layout="wide")
st.markdown("""
    <style>
        .main-container {
            background-color: #f5f5f5;
            padding: 20px;
            border-radius: 10px;
        }
        .analysis-container {
            background-color: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

st.title("📊 FP&A AI-Powered Learning Advisor")
st.write("Answer a few questions to get personalized AI-driven learning recommendations!")

# User Inputs
q1 = st.radio("1. What is your primary goal?", ["Automate financial reporting", "Enhance data analysis", "Build predictive models"], index=0)
q2 = st.radio("2. How comfortable are you with coding?", ["Beginner (No experience)", "Intermediate (Some experience)", "Advanced (Fluent in Python)"], index=0)
q3 = st.radio("3. How much time can you dedicate to learning?", ["A few hours per week", "Several hours per week", "Full-time commitment"], index=0)

# AI Commentary Generation
try:
    client = Groq(api_key=GROQ_API_KEY)
    prompt = f"""
    You are an AI FP&A coach. Based on the user's answers:
    - Recommend whether they should learn Python in Excel, ChatGPT, or Machine Learning.
    - Provide an explanation and next steps.
    Here are their responses:
    1. {q1}
    2. {q2}
    3. {q3}
    """

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a financial planning and analysis (FP&A) learning advisor."},
            {"role": "user", "content": prompt}
        ],
        model="llama3-8b-8192",
    )

    ai_recommendation = response.choices[0].message.content
except Exception as e:
    ai_recommendation = f"Error generating AI response: {e}"

# Display AI Recommendation
st.markdown('<div class="analysis-container">', unsafe_allow_html=True)
st.subheader("🧠 AI-Powered Learning Recommendation")
st.write(ai_recommendation)
st.markdown('</div>', unsafe_allow_html=True)

# Ensure dependencies are installed
try:
    import streamlit as st
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    import os
    from dotenv import load_dotenv
    from groq import Groq
except ImportError as e:
    st.error(f"Missing dependency: {e}. Try installing required packages.")
