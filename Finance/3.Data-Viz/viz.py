import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# File uploader and prompt input
uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])
user_prompt = st.text_input("Enter visualization prompt")

if uploaded_file and user_prompt:
    try:
        # Read the Excel file into df
        df = pd.read_excel(uploaded_file)
        st.write("Data preview:", df.head())  # Verify df is loaded

        # Generate the AI prompt (adjust based on your API)
        ai_prompt = f"""
        Write ONLY a Python function named create_plot that takes a pandas DataFrame df as input and returns a matplotlib figure.
        Do NOT include import statements, comments, or any code outside the function definition.
        Assume pandas as pd and matplotlib.pyplot as plt are already available.
        The DataFrame df has columns: {', '.join(df.columns)}.
        Create a bar chart based on this request: '{user_prompt}'.
        """
        # Simulate API call (replace with your actual API call)
        generated_code = """
def create_plot(df):
    total_sales = df.groupby('category')['sales'].sum()
    fig, ax = plt.subplots()
    total_sales.plot(kind='bar', ax=ax)
    ax.set_title('Total Sales by Category')
    ax.set_xlabel('Category')
    ax.set_ylabel('Sales')
    return fig
        """

        # Set up execution environment
        globals_dict = {"pd": pd, "plt": plt, "df": df}
        locals_dict = {}

        # Execute the generated code
        try:
            st.write("Generated code:", generated_code)  # Debug output
            exec(generated_code, globals_dict, locals_dict)
            if "create_plot" not in locals_dict:
                st.error("Generated code did not define 'create_plot' function.")
            else:
                create_plot = locals_dict["create_plot"]
                fig = create_plot(df)
                st.pyplot(fig)
        except Exception as e:
            st.error(f"Error executing generated code: {str(e)}")

    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
else:
    st.info("Please upload an Excel file and enter a visualization prompt.")
