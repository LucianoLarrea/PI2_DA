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
symbol = st.sidebar.selectbox('Selecciona una acción:', df0['Symbol'].unique())

# Descargar datos 
df = yf.download(symbol, start="2022-09-28", end="2023-03-28")



# Descargar datos del VIX
yahoo_financials = YahooFinancials('^VIX')
current_vix = yahoo_financials.get_current_price()
if current_vix < 20:
    VIX = 'BUY'
elif current_vix > 30:
    VIX = 'SALE'
else: VIX = 'NEUTRAL'

# Calcular RSI de 14 días
rsi = RSIIndicator(df['Close'], window=14, fillna=True)
df['RSI'] = rsi.rsi()
current_rsi = df.iloc[-1]['RSI']
if current_rsi < 30:
    RSI = 'BUY'
elif current_rsi > 70:
    RSI = 'SALE'
else: RSI = 'NEUTRAL'

# Calcular EMA de 30 días
ema = EMAIndicator(df['Close'], window=30, fillna=True)
df['EMA'] = ema.ema_indicator()
current_ema = df.iloc[-1]['EMA']



# Calcular bandas de Bollinger de 20 días
bbands = BollingerBands(df['Close'], window=20, window_dev=2)
df['BBands_20_2_high'] = bbands.bollinger_hband()
df['BBands_20_2_low'] = bbands.bollinger_lband()
current_price = df.iloc[-1]['Close']
within_bbands = (current_price > df.iloc[-1]['BBands_20_2_low']) and (current_price < df.iloc[-1]['BBands_20_2_high'])

# Mostrar los valores
st.write('VIX:', current_vix, VIX)
st.write('RSI:', round(current_rsi, 2),RSI)
st.write('EMA:', round(current_ema, 2))
st.write('BBands_20_2_high:', round(df.iloc[-1]['BBands_20_2_high'], 2))
st.write('BBands_20_2_low:', round(df.iloc[-1]['BBands_20_2_low'], 2))
st.write('Precio actual:', round(current_price, 2))
st.write('El precio actual está dentro de las bandas de Bollinger:', within_bbands)


# Filtrar datos para el último trimestre
df_last_q = df.loc[df.index > (datetime.now() - timedelta(days=180))]

# Calcular bandas de Bollinger para el último trimestre
bbands_last_month = BollingerBands(df_last_q['Close'], window=30, window_dev=2)
df_last_q['BBands_20_2_high'] = bbands_last_month.bollinger_hband()
df_last_q['BBands_20_2_low'] = bbands_last_month.bollinger_lband()

# Calcular EMA de 90 días
ema_30 = EMAIndicator(df_last_q['Close'], window=30, fillna=True)
df_last_q['EMA_30'] = ema_30.ema_indicator()

# Crear gráfico con precios y bandas de Bollinger
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_last_q.index, y=df_last_q['Close'], name='Precio'))
fig.add_trace(go.Scatter(x=df_last_q.index, y=df_last_q['BBands_20_2_high'], name='Banda superior'))
fig.add_trace(go.Scatter(x=df_last_q.index, y=df_last_q['BBands_20_2_low'], name='Banda inferior'))
fig.add_trace(go.Scatter(x=df_last_q.index, y=df_last_q['EMA_30'], name='EMA 30 días'))
fig.update_layout(title=f"Gráfico de precios del último mes con las bandas de Bollinger para {symbol}")
st.plotly_chart(fig)