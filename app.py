import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf

st.title("📈 Trading Dashboard (Live Data)")

# Sidebar inputs
ticker = st.sidebar.text_input("Ticker", "SPY")
start = st.sidebar.date_input("Start Date")
end = st.sidebar.date_input("End Date")

if st.button("Load Data"):
    
    # Download data
    df = yf.download(ticker, start=start, end=end)

    if df.empty:
        st.error("No data found. Check ticker or dates.")
    else:
        st.subheader("Data Preview")
        st.dataframe(df.head())

        # Moving averages
        df['sma'] = df['Close'].rolling(20).mean()
        df['lma'] = df['Close'].rolling(50).mean()

        # Plot
        fig = px.line(df, y=['Close','sma','lma'], title=f"{ticker} Price")
        st.plotly_chart(fig)

        # Strategy
        df['signal'] = (df['sma'] > df['lma']).astype(int)
        df['returns'] = df['Close'].pct_change()
        df['strategy'] = df['returns'] * df['signal'].shift(1)

        total_return = (1 + df['strategy'].fillna(0)).cumprod().iloc[-1] - 1

        st.metric("Total Return", f"{total_return:.2%}")
