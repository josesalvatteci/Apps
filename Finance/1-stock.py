import streamlit as st
import streamlit.components.v1 as components

# Title and description
st.title('FP&A Dashboard with D3.js')
st.write('A simple financial planning and analysis dashboard using D3.js in Streamlit.')

# HTML for D3.js Visualization
html_code = """
<!DOCTYPE html>
<html>
<head>
  <script src="https://d3js.org/d3.v7.min.js"></script>
  <style>
    .bar { fill: steelblue; }
    .bar:hover { fill: orange; }
  </style>
</head>
<body>
  <svg width="500" height="300"></svg>
  <script>
    const data = [30, 80, 45, 60, 20, 90, 55];
    const svg = d3.select("svg"),
          width = +svg.attr("width"),
          height = +svg.attr("height"),
          margin = {top: 20, right: 20, bottom: 30, left: 40},
          barWidth = width / data.length;

    svg.selectAll(".bar")
      .data(data)
      .enter().append("rect")
        .attr("class", "bar")
        .attr("x", (d, i) => i * barWidth)
        .attr("y", d => height - d)
        .attr("width", barWidth - 5)
        .attr("height", d => d)
        .on("mouseover", function() {
          d3.select(this).style("fill", "orange");
        })
        .on("mouseout", function() {
          d3.select(this).style("fill", "steelblue");
        });
  </script>
</body>
</html>
"""

# Render D3.js visualization in Streamlit
components.html(html_code, height=350)
