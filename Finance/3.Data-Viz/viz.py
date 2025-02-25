import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import io
import sys
from groq import Groq
from dotenv import load_dotenv

# **🔐 Load API Key Securely**
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("🚨 API Key is missing! Set it in Streamlit Secrets or a .env file.")
    st.stop()

# **🧠 AI Model Options**
MODEL_OPTIONS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768",
    "llama3-70b-8192"
]

# **🎨 Streamlit UI Styling**
st.set_page_config(page_title="AI-Powered FP&A & Data Visualization", page_icon="📊", layout="wide")

# **🌟 Title**
st.title("🚀 AI-Powered FP&A & Data Visualization")

# **🧠 Select AI Model**
selected_model = st.selectbox("🔍 Choose an AI model:", MODEL_OPTIONS)

# **📂 File Upload**
uploaded_file = st.file_uploader("📂 Upload an Excel or CSV file", type=["xlsx", "csv"])

if uploaded_file:
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith("xlsx") else pd.read_csv(uploaded_file)

    st.write("📊 **Preview of your data:**")
    st.write(df.head())

    # **🔍 Summarize Dataset for AI**
    def summarize_dataframe(df):
        """Creates a summary of the DataFrame for AI context."""
        summary = {
            "Columns": list(df.columns),
            "Data Types": df.dtypes.to_dict(),
            "Missing Values": df.isnull().sum().to_dict(),
            "Sample Data": df.head(3).to_dict(orient="records")
        }
        return summary

    df_summary = summarize_dataframe(df)

    # **📈 AI-Suggested Visualizations**
    st.subheader("🎯 AI-Suggested Visualizations")
    
    client = Groq(api_key=GROQ_API_KEY)
    vis_prompt = f"""
    Given this dataset summary:
    {df_summary}

    Suggest 3 different types of visualizations that would best represent the data.
    Output should be a numbered list of visualization ideas.
    """

    response = client.chat.completions.create(
        model=selected_model,
        messages=[{"role": "system", "content": vis_prompt}]
    )

    vis_suggestions = response.choices[0].message.content
    st.write(vis_suggestions)

    # **🎨 User Prompt for Visualization**
    user_prompt = st.text_area("✍️ Describe your desired visualization", "Create a bar chart of sales by month")

    if st.button("🚀 Generate Chart"):
        # **💡 Generate Python Code for Visualization**
        code_prompt = f"""
        You are a Python coding assistant. The user uploaded a dataset, and here is the summary:
        {df_summary}

        Generate Python code using pandas, matplotlib, and seaborn to create a visualization based on the user's prompt.
        Do not include file upload code; assume 'df' is already loaded. Return only executable Python code.
        """

        response = client.chat.completions.create(
            model=selected_model,
            messages=[
                {"role": "system", "content": code_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )

        generated_code = response.choices[0].message.content

        st.subheader("📝 Generated Python Code")
        st.code(generated_code, language="python")

        # **🛡 Execute Generated Code Safely**
        def execute_code_safely(code, globals_dict):
            """Executes generated code safely and captures stdout/stderr."""
            stdout = io.StringIO()
            stderr = io.StringIO()

            try:
                sys.stdout = stdout
                sys.stderr = stderr
                exec(code, globals_dict)
                result = stdout.getvalue()
            except Exception as e:
                result = f"Error: {str(e)}"
            finally:
                sys.stdout = sys.__stdout__
                sys.stderr = sys.__stderr__

            return result, stderr.getvalue()

        exec_globals = {"df": df, "plt": plt, "pd": pd, "sns": sns}
        output, error = execute_code_safely(generated_code, exec_globals)

        if error:
            st.error(f"❌ Error executing generated code:\n{error}")
        else:
            if "fig" in exec_globals:
                st.subheader("📊 Generated Chart:")
                st.pyplot(exec_globals["fig"])

                # **🛠 Customize the Chart**
                st.subheader("🎛 Customize Your Chart")
                title = st.text_input("Chart Title", "My Chart")
                xlabel = st.text_input("X-axis Label", "X-axis")
                ylabel = st.text_input("Y-axis Label", "Y-axis")

                fig = exec_globals["fig"]
                ax = fig.axes[0] if fig.axes else fig.gca()

                ax.set_title(title)
                ax.set_xlabel(xlabel)
                ax.set_ylabel(ylabel)

                st.pyplot(fig)

                # **💾 Download Options**
                st.subheader("💾 Save & Share")

                img_buffer = io.BytesIO()
                fig.savefig(img_buffer, format="png")
                st.download_button("📥 Download Chart", img_buffer.getvalue(), "chart.png", "image/png")

                st.download_button("📥 Download Python Code", generated_code, "generated_code.py")

# **📖 AI-Generated FP&A Commentary**
st.subheader("📊 AI-Generated FP&A Commentary")

commentary_prompt = f"""
You are the Head of FP&A at a SaaS company. Your task is to analyze the full budget variance table and provide:
- Key insights from the data.
- Areas of concern and key drivers for variance.
- A CFO-ready summary using the Pyramid Principle.
- Actionable recommendations to improve financial performance.

Here is the full dataset in JSON format:
{df.to_json(orient='records')}
"""

response = client.chat.completions.create(
    model=selected_model,
    messages=[
        {"role": "system", "content": "You are a financial planning and analysis (FP&A) expert, specializing in SaaS companies."},
        {"role": "user", "content": commentary_prompt}
    ]
)

ai_commentary = response.choices[0].message.content
st.write(ai_commentary)

# **📌 Credit & Tutorial**
st.markdown("""
---
**🚀 Build with AI by Christian Martinez**  
[🎥 Learn how to create this app](https://youtu.be/ifaRahCTuS0?si=-9celuiwyHrPb94D)
""")
