import streamlit as st
import yfinance as yf
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
from ta.volatility import BollingerBands
from yahoofinancials import YahooFinancials
from datetime import datetime, timedelta
import plotly.graph_objs as go

# Establecer conexión con Yahoo Finance
yf.pdr_override()

df0 = pd.read_parquet('pdata/companies.parquet')
symbol = st.sidebar.selectbox('Select a stock:', df0['Symbol'].unique(),index=25)

# Descargar datos 
df = yf.download(symbol, start="2022-09-28", end="2023-03-28")



# Descargar datos del VIX
yahoo_financials = YahooFinancials('^VIX')
current_vix = yahoo_financials.get_current_price()

if current_vix < 20:
    VIX = ':green[BUY] (Market calm)'
elif current_vix > 30:
    VIX = ':red[SALE] (Market fear)'
else: VIX = 'NEUTRAL'

# Calcular RSI de 14 días
rsi = RSIIndicator(df['Close'], window=14, fillna=True)
df['RSI'] = rsi.rsi()
current_rsi = df.iloc[-1]['RSI']
if current_rsi < 30:
    RSI = ':green[BUY]'
elif current_rsi > 70:
    RSI = ':red[SALE]'
else: RSI = 'NEUTRAL'


# Calcular bandas de Bollinger de 20 días
bbands = BollingerBands(df['Close'], window=20, window_dev=2)
df['BBands_high'] = bbands.bollinger_hband()
df['BBands_low'] = bbands.bollinger_lband()
current_price = df.iloc[-1]['Close']
within_bbands = (current_price > df.iloc[-1]['BBands_low']) and (current_price < df.iloc[-1]['BBands_high'])


# Calcular EMA de 30 días
ema = EMAIndicator(df['Close'], window=30, fillna=True)
df['EMA'] = ema.ema_indicator()
current_ema = df.iloc[-1]['EMA']
if current_ema > current_price:
    EMA = ':green[BUY]'
else: EMA = ':red[SALE]'


# Mostrar los valores
col1, col2 = st.columns(2)
with col1:
    st.subheader('Market indicator')
    st.metric('VIX', current_vix)
    st.markdown(VIX)
    st.markdown("""---""")
    st.subheader('Momentum indicator')
    st.metric('RSI', round(current_rsi, 2))
    st.write(RSI)

with col2:
    st.subheader('Volatility indicator')
    st.write('BBands_high:', round(df.iloc[-1]['BBands_high'], 2))
    st.markdown("""---""")
    st.metric('Price', round(current_price, 2))
    st.markdown("""---""")
    st.write('BBands_low:', round(df.iloc[-1]['BBands_low'], 2))
    st.write('Current price between Bollinger Bands:', within_bbands)
    # st.metric('EMA', round(current_ema, 2))
    # st.write(EMA)

# Filtrar datos para el último semestre
df_last_q = df.loc[df.index > (datetime.now() - timedelta(days=180))]

# Calcular bandas de Bollinger para el último mes
bbands_last_month = BollingerBands(df_last_q['Close'], window=30, window_dev=2)
df_last_q['BBands_high'] = bbands_last_month.bollinger_hband()
df_last_q['BBands_low'] = bbands_last_month.bollinger_lband()

# Calcular EMA de 30 días
ema_30 = EMAIndicator(df_last_q['Close'], window=30, fillna=True)
df_last_q['EMA_30'] = ema_30.ema_indicator()

# Crear gráfico con precios y bandas de Bollinger
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_last_q.index, y=df_last_q['Close'], name='Price'))
fig.add_trace(go.Scatter(x=df_last_q.index, y=df_last_q['BBands_high'], name='Superior Band'))
fig.add_trace(go.Scatter(x=df_last_q.index, y=df_last_q['BBands_low'], name='Inferior Band'))
fig.add_trace(go.Scatter(x=df_last_q.index, y=df_last_q['EMA_30'], name='EMA 30 days'))
fig.update_layout(title=f"Bollinger Bands for {symbol}")
st.plotly_chart(fig)