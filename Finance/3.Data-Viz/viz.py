import streamlit as st
import pandas as pd
import openai
import matplotlib.pyplot as plt
import io
import sys

# Set your Groq API key
GROQ_API_KEY = "your-groq-api-key"

# Function to summarize the DataFrame
def summarize_dataframe(df):
    """Creates a summary of the DataFrame for LLM context."""
    summary = {
        "Columns": list(df.columns),
        "Data Types": df.dtypes.to_dict(),
        "Missing Values": df.isnull().sum().to_dict(),
        "Sample Data": df.head(3).to_dict(orient="records")
    }
    return summary

# Function to suggest visualizations based on data
def suggest_visualizations(df_summary):
    """Asks AI to suggest the best visualizations for the dataset."""
    prompt = f"""
    Given this dataset summary:
    {df_summary}

    Suggest 3 different types of visualizations that would best represent the data.
    Output should be a numbered list of visualization ideas.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": prompt}],
        api_key=GROQ_API_KEY
    )
    
    return response["choices"][0]["message"]["content"]

# Function to generate code using Groq API
def generate_code(prompt, df_summary):
    system_prompt = f"""
    You are a Python coding assistant. The user uploaded a dataset, and here is the summary:
    {df_summary}

    Generate Python code using pandas and matplotlib to create a visualization based on the user's prompt.
    Do not include file upload code; assume 'df' is already loaded. Return only executable Python code.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        api_key=GROQ_API_KEY
    )

    return response["choices"][0]["message"]["content"]

# Function to safely execute generated code
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

# Streamlit UI
st.title("AI-Powered Data Visualization")

uploaded_file = st.file_uploader("Upload an Excel or CSV file", type=["xlsx", "csv"])

if uploaded_file:
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith("xlsx") else pd.read_csv(uploaded_file)
    
    st.write("📊 **Preview of your data:**")
    st.write(df.head())

    # Summarize dataset for AI
    df_summary = summarize_dataframe(df)

    # Suggest visualizations
    st.subheader("🔍 AI-Suggested Visualizations")
    suggestions = suggest_visualizations(df_summary)
    st.write(suggestions)

    # User selects or enters a prompt
    user_prompt = st.text_area("✍️ Describe your visualization", "Create a bar chart of sales by month")

    if st.button("🎨 Generate Chart"):
        code = generate_code(user_prompt, df_summary)

        st.subheader("💡 Generated Python Code:")
        st.code(code, language="python")

        # Execute generated code
        exec_globals = {"df": df, "plt": plt, "pd": pd}
        output, error = execute_code_safely(code, exec_globals)

        if error:
            st.error(f"❌ Error executing generated code:\n{error}")
        else:
            if "fig" in exec_globals:
                st.subheader("📊 Generated Chart:")
                st.pyplot(exec_globals["fig"])

                # Allow customization
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

                # Download options
                st.subheader("💾 Save & Share")

                # Save chart as image
                img_buffer = io.BytesIO()
                fig.savefig(img_buffer, format="png")
                st.download_button("📥 Download Chart", img_buffer.getvalue(), "chart.png", "image/png")

                # Download generated Python code
                st.download_button("📥 Download Python Code", code, "generated_code.py")

# Add credit and tutorial link
st.markdown("""
---
**🚀 Build with AI by Christian Martinez**  
[🎥 Learn how to create this app](https://youtu.be/ifaRahCTuS0?si=-9celuiwyHrPb94D)
""")
