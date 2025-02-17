import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json

# Title and Description
st.title('🌟 FP&A Dashboard with File Upload (D3.js & Streamlit)')
st.write('Upload your Excel file to generate a Financial Planning & Analysis dashboard with interactive D3.js charts.')

# File Upload
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

def load_data(file):
    return pd.read_excel(file) if file else pd.DataFrame()

data = load_data(uploaded_file)

if not data.empty:
    st.dataframe(data)

    # Enhanced D3.js Visualization
    D3_CODE = """
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://d3js.org/d3.v7.min.js"></script>
        <style>
            .bar { fill: #4CAF50; transition: fill 0.3s; }
            .bar:hover { fill: #FF5722; }
            .axis-label { font: 12px sans-serif; }
        </style>
    </head>
    <body>
        <svg width="700" height="450"></svg>
        <script>
            const data = JSON.parse(`$DATA`);
            const margin = {top: 30, right: 40, bottom: 50, left: 60};
            const width = 700 - margin.left - margin.right;
            const height = 450 - margin.top - margin.bottom;

            const svg = d3.select("svg")
                .append("g")
                .attr("transform", `translate(${margin.left},${margin.top})`);

            const x = d3.scaleBand()
                .domain(data.map(d => d.Month))
                .range([0, width])
                .padding(0.3);

            const y = d3.scaleLinear()
                .domain([0, d3.max(data, d => d.Revenue)])
                .nice()
                .range([height, 0]);

            svg.selectAll(".bar")
                .data(data)
                .join("rect")
                .attr("class", "bar")
                .attr("x", d => x(d.Month))
                .attr("width", x.bandwidth())
                .attr("y", height)
                .attr("height", 0)
                .transition()
                .duration(800)
                .attr("y", d => y(d.Revenue))
                .attr("height", d => height - y(d.Revenue));

            svg.append("g")
                .call(d3.axisLeft(y).tickSize(-width).ticks(6))
                .attr("class", "axis-label");
            svg.append("g")
                .attr("transform", `translate(0,${height})`)
                .call(d3.axisBottom(x))
                .attr("class", "axis-label");
        </script>
    </body>
    </html>
    """

    html_code = D3_CODE.replace('$DATA', json.dumps(data.to_dict(orient='records')))
    components.html(html_code, height=500)
else:
    st.warning("Please upload an Excel file with 'Month' and 'Revenue' columns.")
