import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Set page configuration
st.set_page_config(
    page_title="Nibble - FP&A Learning Hub",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E86C1;
        text-align: center;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #5499C7;
        margin-bottom: 1rem;
    }
    .description {
        font-size: 1.1rem;
        color: #1C2833;
    }
    .highlight {
        background-color: #EBF5FB;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .results-container {
        background-color: #F8F9F9;
        padding: 2rem;
        border-radius: 0.5rem;
        margin: 2rem 0;
        border: 1px solid #D5D8DC;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'responses' not in st.session_state:
    st.session_state.responses = []
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'all_responses' not in st.session_state:
    st.session_state.all_responses = []
    
# App Header
st.markdown("<h1 class='main-header'>Nibble</h1>", unsafe_allow_html=True)
st.markdown("<h3 class='sub-header'>FP&A Learning Pathfinder</h3>", unsafe_allow_html=True)
st.markdown("<p class='description'>Get personalized learning recommendations for enhancing your FP&A skills through Python, Excel, ChatGPT, or Machine Learning.</p>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://raw.githubusercontent.com/username/nibble-app/main/logo.png", width=200) # Replace with your GitHub username
    st.markdown("### About Nibble")
    st.write("Nibble helps finance professionals discover the right tools to enhance their analytical capabilities.")
    st.markdown("### Resources")
    st.markdown("- [GitHub Repository](https://github.com/username/nibble-app)") # Replace with your GitHub username
    st.markdown("- [Documentation](https://github.com/username/nibble-app/wiki)") # Replace with your GitHub username
    st.markdown("- [Report Issues](https://github.com/username/nibble-app/issues)") # Replace with your GitHub username
    
    st.markdown("### View Community Results")
    if st.button("See what others are learning"):
        st.session_state.view_results = True
    else:
        st.session_state.view_results = False

# Main content
if st.session_state.get('view_results', False):
    st.markdown("<div class='highlight'>", unsafe_allow_html=True)
    st.markdown("## Community Learning Preferences")
    st.write("See what other FP&A professionals are interested in learning:")
    
    # Create sample data for demonstration
    sample_data = [
        {"role": "Financial Analyst", "years_experience": 2, "learning_focus": "Python", "specific_skill": "Data Cleaning", "time_commitment": "5-10 hours"},
        {"role": "FP&A Manager", "years_experience": 6, "learning_focus": "Excel", "specific_skill": "Advanced Formulas", "time_commitment": "2-5 hours"},
        {"role": "Senior Financial Analyst", "years_experience": 4, "learning_focus": "ChatGPT", "specific_skill": "Report Writing", "time_commitment": "2-5 hours"},
        {"role": "Director of FP&A", "years_experience": 9, "learning_focus": "Machine Learning", "specific_skill": "Forecasting Models", "time_commitment": "10+ hours"},
        {"role": "Financial Controller", "years_experience": 7, "learning_focus": "Python", "specific_skill": "Automation", "time_commitment": "5-10 hours"},
        {"role": "Financial Analyst", "years_experience": 1, "learning_focus": "Excel", "specific_skill": "Pivot Tables", "time_commitment": "2-5 hours"},
        {"role": "FP&A Specialist", "years_experience": 3, "learning_focus": "ChatGPT", "specific_skill": "Data Analysis Prompting", "time_commitment": "2-5 hours"},
    ]
    
    # Add session state responses to sample data
    combined_data = sample_data + st.session_state.all_responses
    
    # Convert to DataFrame
    df = pd.DataFrame(combined_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Learning focus distribution
        st.subheader("Learning Focus Distribution")
        focus_counts = df['learning_focus'].value_counts()
        fig, ax = plt.subplots(figsize=(8, 5))
        focus_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax, colors=sns.color_palette("Blues_r"))
        ax.set_ylabel('')
        st.pyplot(fig)
        
    with col2:
        # Time commitment distribution
        st.subheader("Time Commitment")
        time_counts = df['time_commitment'].value_counts()
        fig, ax = plt.subplots(figsize=(8, 5))
        time_counts.plot(kind='bar', ax=ax, color=sns.color_palette("Blues"))
        ax.set_ylabel('Number of Respondents')
        ax.set_xlabel('Weekly Hours')
        st.pyplot(fig)
    
    # Specific skill word cloud alternative - show popular skills by category
    st.subheader("Popular Skills by Learning Focus")
    
    focus_categories = df['learning_focus'].unique()
    cols = st.columns(len(focus_categories))
    
    for i, focus in enumerate(focus_categories):
        with cols[i]:
            st.markdown(f"**{focus}**")
            focus_skills = df[df['learning_focus'] == focus]['specific_skill'].value_counts().head(5)
            for skill, count in focus_skills.items():
                st.write(f"- {skill} ({count})")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("Take the Survey"):
        st.session_state.view_results = False
else:
    # Survey form
    if not st.session_state.submitted:
        st.markdown("<div class='highlight'>", unsafe_allow_html=True)
        st.markdown("## FP&A Learning Preferences Survey")
        st.write("Answer these questions to get personalized recommendations for your FP&A skill development.")
        
        # Question 1
        st.subheader("Question 1: What is your current role in Finance?")
        role = st.selectbox(
            "Select your current role:",
            ["Financial Analyst", "Senior Financial Analyst", "FP&A Specialist", 
             "FP&A Manager", "Finance Director", "Financial Controller", "CFO", "Other"]
        )
        
        # Question 2
        st.subheader("Question 2: How many years of experience do you have in FP&A?")
        years_experience = st.slider("Years of experience:", 0, 20, 3)
        
        # Question 3
        st.subheader("Question 3: Which of these tools are you most interested in learning to enhance your FP&A capabilities?")
        learning_focus = st.radio(
            "Select your primary learning interest:",
            ["Python", "Excel", "ChatGPT", "Machine Learning"]
        )
        
        # Additional questions based on selection
        if learning_focus == "Python":
            specific_skill = st.multiselect(
                "Which Python skills are you most interested in for FP&A?",
                ["Data Cleaning & Preparation", "Financial Analysis", "Automation", "Visualization", 
                 "Budgeting & Forecasting", "API Integration", "Database Querying"]
            )
        elif learning_focus == "Excel":
            specific_skill = st.multiselect(
                "Which Excel skills are you most interested in enhancing?",
                ["Advanced Formulas & Functions", "Power Query", "Pivot Tables", "Data Modeling", 
                 "VBA Macros", "Financial Modeling", "Power BI Integration"]
            )
        elif learning_focus == "ChatGPT":
            specific_skill = st.multiselect(
                "How would you like to use ChatGPT in your FP&A role?",
                ["Report Writing", "Data Analysis Prompting", "Code Generation", "Financial Commentary", 
                 "Process Documentation", "Complex Calculations", "Presentation Creation"]
            )
        else:  # Machine Learning
            specific_skill = st.multiselect(
                "Which machine learning applications interest you for FP&A?",
                ["Forecasting Models", "Anomaly Detection", "Customer Segmentation", "Predictive Analytics", 
                 "Risk Assessment", "Process Optimization", "Text Analysis"]
            )
        
        # Time commitment
        st.subheader("How much time can you commit to learning each week?")
        time_commitment = st.select_slider(
            "Weekly time commitment:",
            options=["1-2 hours", "2-5 hours", "5-10 hours", "10+ hours"]
        )
        
        # Submit button
        if st.button("Get Recommendations"):
            # Store responses
            st.session_state.responses = {
                "role": role,
                "years_experience": years_experience,
                "learning_focus": learning_focus,
                "specific_skill": ", ".join(specific_skill) if isinstance(specific_skill, list) else specific_skill,
                "time_commitment": time_commitment
            }
            
            # Add to all responses
            st.session_state.all_responses.append(st.session_state.responses)
            
            st.session_state.submitted = True
            st.experimental_rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    else:
        # Recommendations based on responses
        st.markdown("<div class='results-container'>", unsafe_allow_html=True)
        st.markdown("## Your Personalized Learning Pathway")
        st.write(f"Based on your profile as a **{st.session_state.responses['role']}** with **{st.session_state.responses['years_experience']} years** of experience, here are your tailored recommendations for learning **{st.session_state.responses['learning_focus']}**.")
        
        # Create learning pathway recommendations based on responses
        learning_focus = st.session_state.responses['learning_focus']
        time_commitment = st.session_state.responses['time_commitment']
        
        st.markdown("### Recommended Learning Path")
        
        if learning_focus == "Python":
            st.markdown("""
            #### Python for FP&A Professionals
            
            1. **Getting Started (Week 1-2)**
               - Setup Python environment with Anaconda
               - Basic Python syntax and data structures
               - Introduction to Pandas for financial data analysis
            
            2. **Core Skills (Week 3-4)**
               - Data cleaning and preparation with Pandas
               - Financial calculations and time series analysis
               - Data visualization with Matplotlib and Seaborn
            
            3. **Advanced Applications (Week 5-6)**
               - Automating financial reports with Python
               - Building forecasting models
               - API integration with financial data sources
            
            4. **Project Implementation (Week 7-8)**
               - Building an automated financial dashboard
               - Creating a budget variance analysis tool
               - Implementing a forecasting model for your business
            """)
            
            # Resources section
            st.markdown("### Recommended Resources")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Courses")
                st.markdown("- [Python for Finance on Coursera](https://www.coursera.org)")
                st.markdown("- [Financial Analysis with Python on Udemy](https://www.udemy.com)")
                st.markdown("- [FP&A Python Bootcamp on DataCamp](https://www.datacamp.com)")
            
            with col2:
                st.markdown("#### Books & Tutorials")
                st.markdown("- *Python for Finance* by Yves Hilpisch")
                st.markdown("- *Financial Modeling in Python* handbook")
                st.markdown("- [Real Python's Financial Analysis Guide](https://realpython.com)")
        
        elif learning_focus == "Excel":
            st.markdown("""
            #### Advanced Excel for FP&A Professionals
            
            1. **Advanced Formula Techniques (Week 1-2)**
               - Complex formula combinations (INDEX/MATCH, OFFSET, etc.)
               - Array formulas and dynamic arrays
               - Financial functions for FP&A applications
            
            2. **Data Modeling & Analysis (Week 3-4)**
               - Building 3-statement financial models
               - Sensitivity and scenario analysis
               - Power Query for data transformation
            
            3. **Automation & Efficiency (Week 5-6)**
               - VBA macros for financial reports
               - Power Pivot for data modeling
               - Creating automated dashboards
            
            4. **Integration & Advanced Applications (Week 7-8)**
               - Excel and Power BI integration
               - Building Monte Carlo simulations
               - Advanced dynamic dashboards
            """)
            
            # Resources section
            st.markdown("### Recommended Resources")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Courses")
                st.markdown("- [Excel Skills for Finance Professionals on LinkedIn Learning](https://www.linkedin.com/learning)")
                st.markdown("- [Financial Modeling in Excel on CFI](https://corporatefinanceinstitute.com)")
                st.markdown("- [Advanced Excel for FP&A on Udemy](https://www.udemy.com)")
            
            with col2:
                st.markdown("#### Books & Tutorials")
                st.markdown("- *Financial Modeling and Valuation* by Paul Pignataro")
                st.markdown("- *Advanced Excel Essentials* by Jordan Goldmeier")
                st.markdown("- [ExcelJet's Advanced Formula Guide](https://exceljet.net)")
        
        elif learning_focus == "ChatGPT":
            st.markdown("""
            #### ChatGPT for FP&A Professionals
            
            1. **Fundamentals of AI Prompting (Week 1-2)**
               - Understanding ChatGPT capabilities and limitations
               - Learning effective prompt engineering
               - Basic financial analysis prompts
            
            2. **Financial Analysis Applications (Week 3-4)**
               - Creating templates for recurring financial analysis
               - Using ChatGPT for financial commentary generation
               - Data interpretation and insight extraction
            
            3. **Automation & Integration (Week 5-6)**
               - Combining ChatGPT with Excel using APIs
               - Automating routine analysis and reporting
               - Building process documentation flows
            
            4. **Advanced Applications (Week 7-8)**
               - Financial forecasting assistance
               - Variance analysis and root cause identification
               - Creating presentation narratives and executive summaries
            """)
            
            # Resources section
            st.markdown("### Recommended Resources")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Courses & Tutorials")
                st.markdown("- [Prompt Engineering for Finance Professionals](https://www.promptingguide.ai)")
                st.markdown("- [ChatGPT for Financial Analysis on Udemy](https://www.udemy.com)")
                st.markdown("- [AI for Finance Professionals on Coursera](https://www.coursera.org)")
            
            with col2:
                st.markdown("#### Tools & Templates")
                st.markdown("- [FP&A Prompt Library](https://github.com/username/fpa-prompts)") # Replace with your GitHub username
                st.markdown("- ChatGPT plugin for financial data analysis")
                st.markdown("- Excel-ChatGPT integration templates")
        
        else:  # Machine Learning
            st.markdown("""
            #### Machine Learning for FP&A Professionals
            
            1. **Foundations (Week 1-3)**
               - Basic statistical concepts for ML
               - Introduction to Python for ML (NumPy, Pandas, Scikit-learn)
               - Data preparation for financial modeling
            
            2. **Core ML Techniques (Week 4-6)**
               - Regression models for forecasting
               - Classification for risk assessment
               - Time series analysis for financial data
            
            3. **Financial Applications (Week 7-9)**
               - Building revenue forecasting models
               - Customer segmentation and analysis
               - Anomaly detection for financial data
            
            4. **Advanced Implementation (Week 10-12)**
               - Model evaluation and improvement
               - Deploying ML models in business context
               - Creating ML-powered financial dashboards
            """)
            
            # Resources section
            st.markdown("### Recommended Resources")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Courses")
                st.markdown("- [Machine Learning for Finance on DataCamp](https://www.datacamp.com)")
                st.markdown("- [Financial Forecasting with ML on Coursera](https://www.coursera.org)")
                st.markdown("- [ML for Business Finance on edX](https://www.edx.org)")
            
            with col2:
                st.markdown("#### Books & Tutorials")
                st.markdown("- *Machine Learning for Financial Risk Management* by Abdullah Karasan")
                st.markdown("- *Python Machine Learning for Finance* by Jannes Klaas")
                st.markdown("- [Towards Data Science - Finance ML articles](https://towardsdatascience.com)")
        
        # Feedback and social sharing
        st.markdown("### Share Your Learning Journey")
        st.write("Connect with other FP&A professionals on the same learning path:")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("Share on LinkedIn")
        with col2:
            st.button("Join Discord Community")
        with col3:
            st.button("Find a Study Group")
        
        # Reset and view community results
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Retake Survey"):
                st.session_state.submitted = False
                st.experimental_rerun()
        with col2:
            if st.button("View Community Results"):
                st.session_state.submitted = False
                st.session_state.view_results = True
                st.experimental_rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center;">
        <p>© 2025 Nibble - FP&A Learning Hub | 
        <a href="https://github.com/username/nibble-app">GitHub</a> | 
        <a href="https://github.com/username/nibble-app/issues">Report Issues</a></p>
    </div>
    """, 
    unsafe_allow_html=True
)
