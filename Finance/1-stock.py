import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import datetime

# App Title
st.title('🚀 Advanced Finance Dashboard: Stock Market Analysis')

# Sidebar Controls
ticker = st.sidebar.text_input('Stock Ticker (e.g., AAPL, TSLA):', 'AAPL')
start_date = st.sidebar.date_input('Start Date', datetime.date(2020, 1, 1))
end_date = st.sidebar.date_input('End Date', datetime.date.today())
indicator = st.sidebar.selectbox('Select Indicator', ['SMA', 'EMA', 'Bollinger Bands'])

# Fetch Stock Data
@st.cache_data
def get_stock_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end)
    data.columns = [col if isinstance(col, str) else col[1] for col in data.columns]
    return data

stock_data = get_stock_data(ticker, start_date, end_date)

# Raw Data Table
st.subheader(f'📄 {ticker} Data')
st.data_editor(stock_data)

# Price Chart with Indicators
st.subheader('📈 Price Chart with Indicators')
fig = px.line(stock_data, x=stock_data.index, y='Close', title=f'{ticker} Closing Prices')

if indicator == 'SMA':
    stock_data['SMA_20'] = stock_data['Close'].rolling(window=20).mean()
    fig.add_scatter(x=stock_data.index, y=stock_data['SMA_20'], mode='lines', name='20-Day SMA')
elif indicator == 'EMA':
    stock_data['EMA_20'] = stock_data['Close'].ewm(span=20, adjust=False).mean()
    fig.add_scatter(x=stock_data.index, y=stock_data['EMA_20'], mode='lines', name='20-Day EMA')
else:
    rolling_mean = stock_data['Close'].rolling(window=20).mean()
    rolling_std = stock_data['Close'].rolling(window=20).std()
    fig.add_scatter(x=stock_data.index, y=rolling_mean + 2*rolling_std, mode='lines', name='Upper Band')
    fig.add_scatter(x=stock_data.index, y=rolling_mean - 2*rolling_std, mode='lines', name='Lower Band')

st.plotly_chart(fig)

# Volume Analysis
st.subheader('📊 Volume Analysis')
fig_volume = px.bar(stock_data, x=stock_data.index, y='Volume', title=f'{ticker} Trading Volume')
st.plotly_chart(fig_volume)

# Financial Metrics Summary
st.subheader('💰 Financial Metrics')
st.metric(label="Latest Close Price", value=f"${stock_data['Close'].iloc[-1]:.2f}")
st.metric(label="Average Volume", value=f"{stock_data['Volume'].mean():,.0f}")

# Correlation Heatmap
st.subheader('🔥 Correlation Heatmap')
plt.figure(figsize=(6, 4))
sns.heatmap(stock_data.corr(), annot=True, cmap='coolwarm')
st.pyplot(plt)

# Footer
st.text('💎 Powered by Streamlit, Yahoo Finance API, Plotly, and Matplotlib.')
