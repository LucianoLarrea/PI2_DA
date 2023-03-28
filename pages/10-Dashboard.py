import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
import pandas_ta as ta
import datetime

st.title('Dashboard')
ticker = st.sidebar.selectbox('Ticker',['^GSPC','AAPL','GPRO'])
start_date = st.sidebar.date_input('Start Date',datetime.date(2013, 1, 1))
end_date = st.sidebar.date_input('End Date',datetime.date(2023, 1, 1)) 

data = yf.download(ticker,start=start_date,end=end_date)
fig = px.line(data,x=data.index,y=data['Adj Close'],title=ticker)
st.plotly_chart(fig)

pricing,fundamental,technical,chatGPT = st.tabs(['Pricing','Fundamental Analysis','Technical Analysis','chatGPT'])

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
    technical_indicator = st.selectbox('Tech Indicator',options=KPI_list)
    method = technical_indicator                                  # Elige un indicador
    indicator = pd.DataFrame(                       # Toma los atributos necesarios para calcular
        getattr(ta,method)(low=data['Low'],close=data['Close'],high=data['High'],open=data['Open'],volume=data['Volume'],))
    indicator['Close'] = data['Close']
    figW_KPI_new = px.line(indicator)               # Grafica Close vs Indicados
    st.plotly_chart(figW_KPI_new)
    st.write(indicator)

with chatGPT:
    from pyChatGPT import ChatGPT
    st.write('chatGPT')
    session_token = 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0.._ZNaNTQ-8u9iZ47s.XwhAfoHQBsXoP5xs7T6E1n76US2nTLaIRQTtr_S1zWGllFCHFg6fuZLQWBUdF1Sntx_e9BkxH5eJBXHmvtn6Hr3X_im8p3AzcoZyjeQwtLXN2zdEqTafMNOa4XVfI7bpKVWxwx_iaTaWi08fmuw1EDAHmgDvtw__4u9LcC9RbFk1ryFCS4CV0D18FGZCJ5TMqREpJKR426CLpFOSpREnqDqOyTdcv4tw2pkqz24rvahglTG4p5biwU0UW_twT10JD8UBJj6NzZvW5VkmDinuTRX4Hxcpj8HK05mjN89fAUQhKYbLCOwYVQLfX1pJqEXlJ8BcCjPkgmnHjL3yd9-sldagSI4bZFI_1A8NfCsm0DamUuLrb2N59zCWWJwvQT5X7RSA1Z8BIvTS0lSsBT_Ybvbcup7VJ9UWmwK4vVPQJ2QPBuY7KBXW6jiJUIlR_WQF1CUyjfp2SUkaNmAx8GivrikOcVMTtlascixDDamUY8CMEohK52X1cDeNGdmcR40E0rX8gOG2V6Nff9PlGHebxdLQFQXFeHl9ZV0uYEVbzh7UuYKaNJGPpMOKPxHnx0pdSgOjdtzsoacjhjCfrwZBP1DpJKS-lUwntqhdiQw8EDeKll7AdKrzmNFcioBzshiUbCbN-tvorKR3mz1c5LHNrZTWkirqQJVI8Xaf5PC6mtpqA1DmaluS8-EBe7q_XzjC5sSnnxcul9ruGE9EaDx-6GoP-NyQp7aAkgw5dsv5mEgx0VX3bTdE9qo-F1GT9JgAR3s5Hm6DM2UPCwbXBPS5T-ADmGtAXJhMW6kAed_NctYgSAScOmMG83fHiGRs45BVNf3g-ei1U5bgD9wVFeC90GlGmj3IZo5_-vETXR5sgcPWykpXWU2K76D5gOKmUlP747PUusZVS2Xx5jIOLwJNX9LYiiolWy7rZU9qVSkDRs1lyTlUs15vgQphbfAzEhCQ8kwpnBCGEspd2YdX2WzhTPVgfbFdQMNd_2q80kxF1f__z8hoo8T8psYOi2-6Y8veFD20kYp9p_24-8K2qzl9fBeVzDlXPGZvrkKoupQA4vKvyXYWTi0NSfCASxSGXRtPTM7_eN9yRQq9QwBVxX21MgpievE8jflUdW0mZUyk_B5lhsJTzlRm-qOqxw96hW-y_3u9Ob2GWnVELIuXHEeyPj2ikxJZzPvKKGTBPVjB3b0svR06B1p9OxQ8hp7TnumxN4NgDT8lfIEytRfyQhmIgVmFL0gn54gwD50Qve_peJ5aHDXWX-4QEgmDwe6jJND21gPF0-6rhZtBSpk8pLm6hdzmTrLcr376R8GzDnLjgJpxHwY7TfjH-tPmoapRdJdBdYREww7vxE_9_dHOwszx5LJIKLRNXOJdH2xLfPI0nw4a6Ua7SSHrHzohxc5BsJEh2wac7oSDMy2QTgfuglR2xKQz-RnmE3LIGmj4Q0jjkmVp1r5-jSvm_kvi80ditcIpyC435_jWnnxYxAivNHkO_XPid0a9eirGzC9aDzY0dAoAeTXrgiGjRfS1FXuIn4_wZXXIXIcGor9PJVZrpo0GCE7iRb3I3ltkZqygS11gYN1rx3UVZPFBwua7XJ2nepbssFL4gt6xjfFuP3UIUir_RD1jggtrVWXwxsPMI3nV3bNKsz-7vdnUTbDjo6sh6PXny6dFwItCT7GsT14hSI2G3Uj_2kcPZX4640H88gV8JfONuaaB7wwc3sdlLvED6Qb-YG087P4lHs0vOR7gMEHqjZk7tMb0m-kRJvmBPN9h4b7zmKI9pMAspYfjQk27wKp2AShiKMnDn1tihwMfO3WDfY0LXyfOyGcgs3RfFETw0rqIw8t6-dIqU2JGYtHNuBq904zbqHL_UCi63YKv8312hP6KRQJQt18_wxetPCGvGucZj_WSQjqf_QvysgtOT4cxBpqX0EWWhcQZnsUF81PizmTTf8X21orcL67o7LcI8dgIxu_8GBLdYL87NyaZrGlJu6sBD1JMM58EQvNukUDjGhXCqUa02WUml54OVi4cN1C9JSHzHe0BaQJ-BZaUYRgG1zjYwaG0a80FajEOvWktznNV8-AAPh9mtx8plFT7MiR_717DKqH6B_1QP5fEpccrgRZyqYpUX2GPFSMCsH9UPnVh3aCpfhcVn1k_RSnngHwpbolzAMatG-LAGKhQFLdqmEw3GGvxVas5IxKO3dgKJvIDuf1VmyLansINleFE9vqA8a3pROd6KVYSvosm6M_iYx9Vf1EH_TJ0LRa4NFKTYhfZvztE7KKtgwdyAuslsf9hcB55jvlvLTCarb3CMDhCzJiOLQIPEaGfIRU1Hy4C3JRkIuKt6GoLB8UB7Y7KbP_Lkm6ny3ZyQaYpijaigf1dgsFBSNZEJrgeQnOD5Qz5VU2c7VjZZZFgkAuvp6H5paOmjVwql9-xC8hxl6T_UIV_vcJreconU5RBmfDno8TllX58XBXYGyMxnDMjNiQgId8HKiqo-7apDGGTxyJbhgpq2eiY43A3.GPubMaeWEHaPGf7DtYGkMw'
    api2 = ChatGPT(session_token)
    buy = api2.send_message(f'Which company is {ticker} stock')
    # sell = api2.send_message(f'3 reasons to sell {ticker} stock')
    # swot = api2.send_message(f'SWOT analysis of {ticker} stock')
    st.write(buy['message'])