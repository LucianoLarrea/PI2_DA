import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import datetime
import plotly.express as px
from ta.momentum import RSIIndicator

df = pd.read_parquet('pdata/companies.parquet')
symbol = st.sidebar.selectbox('Selecciona una acción:', df['Symbol'].unique())
start_date = st.sidebar.date_input('Start Date',datetime.date(2013, 1, 1))
end_date = st.sidebar.date_input('End Date',datetime.date(2023, 1, 1)) 

if symbol:
    df = yf.download(symbol, start=start_date, end=end_date)
    
    fig = px.line(df,x=df.index,y=df['Adj Close'],title=symbol)
    st.plotly_chart(fig)
    
    rsi = RSIIndicator(df["Close"])
    df["RSI"] = rsi.rsi()
  
    fig, ax = plt.subplots()



    st.header(f"Technical Analysis {symbol}")
    st.line_chart(df["Close"])
    st.line_chart(df["RSI"])
    options = st.multiselect('Select:',['Price', 'RSI'], ['RSI'])
    if 'Price' in options:
        ax.plot(df["Close"], label="Close Price")
        ax.set_ylabel("Price")
        ax.legend(loc="upper left")

    

    if 'RSI' in options:
        ax2 = ax.twinx()
        ax2.plot(df["RSI"], color="red", label="RSI")
        ax2.axhline(30, color="green", linestyle="--")
        ax2.axhline(70, color="red", linestyle="--")
        ax2.set_ylabel("RSI")
        ax2.legend(loc="upper right")

    st.pyplot(fig)
