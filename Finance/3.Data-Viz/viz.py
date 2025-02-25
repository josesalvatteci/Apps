import streamlit as st

def main():
    st.title("FP&A Learning Recommendation")
    st.write("Answer 3 quick questions to find out what you should learn!")
    
    # Question 1
    q1 = st.radio(
        "1. What is your primary goal?",
        ["Automate financial reporting", "Enhance data analysis", "Build predictive models"],
    )
    
    # Question 2
    q2 = st.radio(
        "2. How comfortable are you with coding?",
        ["Beginner (No experience)", "Intermediate (Some experience)", "Advanced (Fluent in Python)"],
    )
    
    # Question 3
    q3 = st.radio(
        "3. How much time can you dedicate to learning?",
        ["A few hours per week", "Several hours per week", "Full-time commitment"],
    )
    
    # Determine recommendation
    if q1 == "Automate financial reporting":
        recommendation = "Learn Python in Excel! It's perfect for automating reports and financial analysis within a familiar environment."
    elif q1 == "Enhance data analysis":
        recommendation = "Learn ChatGPT! It can help with financial insights, data summarization, and automating repetitive tasks."
    elif q1 == "Build predictive models":
        recommendation = "Learn Machine Learning! It enables forecasting and deeper financial insights for strategic planning."
    
    # Show recommendation
    if st.button("Get My Recommendation"):
        st.success(recommendation)
    
if __name__ == "__main__":
    main()
