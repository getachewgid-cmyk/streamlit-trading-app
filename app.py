import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
import datetime

st.title("📈 Trading Dashboard (Live Data)")

ticker = st.sidebar.text_input("Ticker", "SPY")
start = st.sidebar.date_input("Start Date", datetime.date(2020,1,1))
end = st.sidebar.date_input("End Date", datetime.date.today())

if st.button("Load Data"):

    df = yf.download(ticker, start=start, end=end)

       if df.empty:
        st.error("No data found.")
        st.stop()

 if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
     
    # Indicators
    df['sma'] = df['Close'].rolling(20).mean()
    df['lma'] = df['Close'].rolling(50).mean()

    df = df.dropna()

    st.write(df.columns)

    fig = px.line(
        df,
        x=df.index,
        y=df[['Close','sma','lma']],
        title=f"{ticker} Price"
    )

    st.plotly_chart(fig)

    df['signal'] = (df['sma'] > df['lma']).astype(int)
    df['returns'] = df['Close'].pct_change()
    df['strategy'] = df['returns'] * df['signal'].shift(1)

    total_return = (1 + df['strategy'].fillna(0)).cumprod().iloc[-1] - 1

    st.metric("Total Return", f"{total_return:.2%}")
