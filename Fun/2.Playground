import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
from groq import Groq  # Ensure groq is installed and configured

# -------------------------------
# Setup & Environment
# -------------------------------
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("🚨 API Key is missing! Set it in Streamlit Secrets or a .env file.")
    st.stop()

st.title("📊 FP&A Agent with Advanced AI Reasoning")
st.write("Input your financial metrics for analysis and receive AI-generated insights using advanced reasoning strategies.")

# -------------------------------
# 1️⃣ Choose the Right LLM
# In this example, we use the Groq API (you can swap with any LLM API that supports chain-of-thought prompting).
# -------------------------------

# -------------------------------
# 2️⃣ Define the Agent’s Control Logic
# Set up our FP&A inputs and calculations.
# -------------------------------
st.subheader("Input Financial Metrics")

# Basic FP&A inputs
revenue_growth = st.number_input("Projected Revenue Growth (%)", value=10.0, step=0.5)
initial_revenue = st.number_input("Initial Revenue (in millions)", value=50.0, step=1.0)
cogs_pct = st.number_input("COGS as % of Revenue", value=40.0, step=0.5)
opex_pct = st.number_input("Operating Expenses as % of Revenue", value=20.0, step=0.5)
forecast_years = st.slider("Forecast Period (years)", 1, 10, 5)

# Forecast calculations
years = list(range(1, forecast_years + 1))
forecast_revenue = [initial_revenue * ((1 + revenue_growth/100.0) ** year) for year in years]
forecast_cogs = [rev * (cogs_pct/100.0) for rev in forecast_revenue]
forecast_opex = [rev * (opex_pct/100.0) for rev in forecast_revenue]
forecast_ebitda = [rev - cogs - opex for rev, cogs, opex in zip(forecast_revenue, forecast_cogs, forecast_opex)]

df_forecast = pd.DataFrame({
    "Year": years,
    "Revenue (M)": forecast_revenue,
    "COGS (M)": forecast_cogs,
    "OpEx (M)": forecast_opex,
    "EBITDA (M)": forecast_ebitda
})

st.subheader("Forecasted Financials")
st.dataframe(df_forecast)

# Visualization of the forecasts
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(years, forecast_revenue, marker='o', label="Revenue")
ax.plot(years, forecast_ebitda, marker='o', label="EBITDA")
ax.set_xlabel("Year")
ax.set_ylabel("Amount (in millions)")
ax.set_title("Financial Forecast")
ax.legend()
st.pyplot(fig)

# -------------------------------
# 3️⃣ Define Core Instructions & Features
# Prepare a summary of the FP&A projections for the AI agent.
# -------------------------------
fp_a_summary = f"""
**FP&A Financial Projections Summary:**

- **Forecast Period:** {forecast_years} years
- **Initial Revenue:** {initial_revenue} million
- **Projected Revenue Growth:** {revenue_growth}%
- **COGS as % of Revenue:** {cogs_pct}%
- **Operating Expenses as % of Revenue:** {opex_pct}%

**Forecasted Figures:**
- Revenue over years: {[f'{r:.2f}' for r in forecast_revenue]}
- EBITDA over years: {[f'{e:.2f}' for e in forecast_ebitda]}
"""

st.markdown(fp_a_summary)

# -------------------------------
# 4️⃣ Implement a Memory Strategy
# Using Streamlit session_state to retain recent interactions.
# -------------------------------
if "memory" not in st.session_state:
    st.session_state.memory = []

# -------------------------------
# 5️⃣ Equip the Agent with Tools & APIs
# We use the Groq API to simulate external tool calls.
# -------------------------------
st.subheader("🤖 AI Agent Commentary on FP&A Analysis")
user_prompt = st.text_area("Ask the FP&A Agent:",
                           "Please analyze the financial projections, identify potential risks, and suggest improvement strategies. Explain your reasoning step-by-step.")

# -------------------------------
# 6️⃣ Define the Agent’s Role & Key Tasks
# Construct a prompt that details the agent’s mission and context.
# -------------------------------
if st.button("Generate AI Insights"):
    # Save the current summary to memory for context.
    st.session_state.memory.append(fp_a_summary)
    # Limit memory to the most recent three interactions.
    memory_summary = "\n".join(st.session_state.memory[-3:])

    ai_input = f"""
    You are a seasoned FP&A financial analyst with expertise in scenario analysis and forecasting.
    
    **Agent Memory:**
    {memory_summary}
    
    **Current Financial Projections:**
    {fp_a_summary}
    
    **User Query:**
    {user_prompt}
    
    Please provide detailed analysis, highlight key financial insights, potential risks, and recommend actionable strategies. Use a chain-of-thought approach to explain your reasoning.
    """
    
    # -------------------------------
    # 7️⃣ Handling Raw LLM Outputs
    # Process the AI response for clarity and structure.
    # -------------------------------
    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an expert FP&A analyst. Provide structured, clear analysis with chain-of-thought reasoning."},
            {"role": "user", "content": ai_input}
        ],
        model="llama3-8b-8192",
    )
    ai_commentary = response.choices[0].message.content
    st.markdown("### AI-Generated FP&A Insights")
    st.write(ai_commentary)

# -------------------------------
# 8️⃣ Scaling to Multi-Agent Systems (Advanced)
# In a production scenario, you might coordinate multiple agents, manage shared context, and handle errors between them.
# This section is reserved for future enhancements.
# -------------------------------
