import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
import pandas_ta as ta
import datetime


st.title('Dashboard')
df0 = pd.read_parquet('pdata/companies.parquet')
ticker = st.sidebar.selectbox('Select a stock:', df0['Symbol'].unique(),index=25)
# ticker = st.sidebar.selectbox('Ticker',['^GSPC','AAPL','GPRO'])
start_date = st.sidebar.date_input('Start Date',datetime.date(2013, 1, 1))
end_date = st.sidebar.date_input('End Date',datetime.date(2023, 1, 1)) 

data = yf.download(ticker,start=start_date,end=end_date)
fig = px.line(data,x=data.index,y=data['Adj Close'],title=ticker)
st.plotly_chart(fig)

pricing,fundamental,technical = st.tabs(['Pricing','Fundamental Analysis','Technical Analysis'])

with pricing:
    st.header('Price movements')
    df = data.copy()
    df['% change'] = (df['Adj Close']/df['Adj Close'].shift(1)-1)*100 # Diferencia intradiaria
    df.dropna(inplace=True)
    st.write(df)

    annual_returns = df['% change'].groupby(df.index.year).sum() # Retorno anual no esta en porcentaje (multiplicar por 100)
    st.write('Annual returns')
    st.write(annual_returns)
    
# from stocknews import StockNews
# with news:
#     st.header(f'News of{ticker}')
#     import ssl
#     ssl._create_default_https_context = ssl._create_unverified_context
#     sn = StockNews(ticker, save_news=False)
#     df_news = sn.read_rss()
#     for i in range(5):
#         st.subheader(f'News {i+1}')
#         st.write(df_news['published'][i])
#         st.write(df_news['title'][i])
#         st.write(df_news['summary'][i])
#         title_sentiment = df_news['sentiment_title'][i]
#         st.write(f'Title sentiment {title_sentiment}')
#         news_sentiment = df_news['sentiment_summary'][i]
#         st.write(f'News sentiment {news_sentiment}')
#     ssl._create_default_https_context = ssl._create_default_https_context
    
    
with fundamental:
    from alpha_vantage.fundamentaldata import FundamentalData
    if ticker != '^GSPC':
        key = 'QUJE9PQIH3O7OHYJ'
        fd = FundamentalData(key,output_format='pandas')
        
        balance, income, cashflow = st.tabs(['Balance Sheet','Income Statement','Cashflow Statement'])
        with balance:
            st.subheader('Annual Balance Sheet')
            balance_sheet = fd.get_balance_sheet_annual(ticker)[0]
            bs = balance_sheet.T[2:]
            bs.columns = list(balance_sheet.T.iloc[0])
            st.write(bs)
        with income:
            st.subheader('Annual Income Statement')
            income_statement = fd.get_income_statement_annual(ticker)[0]
            ist = income_statement.T[2:]
            ist.columns = list(income_statement.T.iloc[0])
            st.write(ist)
        with cashflow:
            st.subheader('Annual Cashflow Statement')
            cashflow_statement = fd.get_cash_flow_annual(ticker)[0]
            cs = cashflow_statement.T[2:]
            cs.columns = list(cashflow_statement.T.iloc[0])
            st.write(cs)
        
        
    else: st.write('Make your own Funadamental Analysis')
    
with technical:
    st.write('Tecnical Analysis')
    df1 = pd.DataFrame()
    KPI_list = df1.ta.indicators(as_list=True)      # Lista de indicadores disponibles
    technical_indicator = st.selectbox('Tech Indicator',options=KPI_list, index=14)
    method = technical_indicator                                  # Elige un indicador
    indicator = pd.DataFrame(                       # Toma los atributos necesarios para calcular
        getattr(ta,method)(low=data['Low'],close=data['Close'],high=data['High'],open=data['Open'],volume=data['Volume'],))
    indicator['Close'] = data['Close']
    figW_KPI_new = px.line(indicator)               # Grafica Close vs Indicados
    st.plotly_chart(figW_KPI_new)
    st.write(indicator)

