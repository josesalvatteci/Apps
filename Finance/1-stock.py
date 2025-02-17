import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json

# Title and Description
st.title('FP&A Dashboard with D3.js')
st.write('Interactive Financial Planning & Analysis (FP&A) dashboard powered by D3.js and Streamlit.')

# Sample Data
@st.cache
def load_data():
    return pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
        'Revenue': [10000, 12000, 15000, 13000, 17000],
        'Expense': [8000, 9500, 11000, 10500, 12500]
    })

data = load_data()
st.dataframe(data)

# D3.js Visualization
D3_CODE = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        .bar { fill: steelblue; }
        .bar:hover { fill: orange; }
        .label { fill: white; font: 10px sans-serif; }
    </style>
</head>
<body>
    <svg width="600" height="400"></svg>
    <script>
        const data = JSON.parse(`$DATA`);
        const margin = {top: 20, right: 30, bottom: 30, left: 40};
        const width = 600 - margin.left - margin.right;
        const height = 400 - margin.top - margin.bottom;

        const svg = d3.select("svg")
            .append("g")
            .attr("transform", `translate(${margin.left},${margin.top})`);

        const x = d3.scaleBand()
            .domain(data.map(d => d.Month))
            .range([0, width])
            .padding(0.2);

        const y = d3.scaleLinear()
            .domain([0, d3.max(data, d => d.Revenue)])
            .nice()
            .range([height, 0]);

        svg.append("g")
            .selectAll("rect")
            .data(data)
            .join("rect")
            .attr("class", "bar")
            .attr("x", d => x(d.Month))
            .attr("y", d => y(d.Revenue))
            .attr("height", d => height - y(d.Revenue))
            .attr("width", x.bandwidth());

        svg.append("g")
            .call(d3.axisLeft(y));

        svg.append("g")
            .attr("transform", `translate(0,${height})`)
            .call(d3.axisBottom(x));
    </script>
</body>
</html>
"""

# Pass data to D3
html_code = D3_CODE.replace('$DATA', json.dumps(data.to_dict(orient='records')))
components.html(html_code, height=450)
