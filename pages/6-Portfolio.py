import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as  np
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
from ta.volatility import BollingerBands
from yahoofinancials import YahooFinancials
import datetime
import plotly.graph_objs as go

# Establecer conexión con Yahoo Finance
yf.pdr_override()

df0 = pd.read_parquet('pdata/companies.parquet')
symbol = st.sidebar.selectbox('Selecciona una acción:', df0['Symbol'].unique())

# Obtener la fecha actual
today = datetime.date.today()

# Definir la fecha de inicio predeterminada
start_date_default = datetime.date(2013, 3, 1)

# Crear una entrada de fecha para que el usuario seleccione la fecha de inicio
start_date = st.sidebar.date_input('Start Date', start_date_default)

# Verificar que la fecha seleccionada por el usuario sea válida
if start_date is None or start_date > today:
    start_date = start_date_default


# start_date = st.sidebar.date_input('Start Date',datetime.date(2010, 1, 1))
end_date = st.sidebar.date_input('End Date',datetime.date(2023, 3, 1)) 

# Descargar datos 
df = yf.download(symbol, start=start_date, end=end_date)


# Crear una lista de opciones de activos para el usuario
options = df0['Symbol'].unique().tolist()
options.extend(['BONDS', 'SP500'])

col1, col2 = st.columns(2)
with col1:

    # Crear campos de entrada para que el usuario especifique la proporción de cada activo
    capital = st.number_input('Invested capital',min_value=1000, max_value=1000000, value=1000, step=100)
    cap_stocks = st.number_input("Stock capital (Max 50%)", min_value=0.0, max_value=capital/2, value=0.0,step=100.0)
    # cap_stocks = st.slider("Stock capital (Max 50%)", 0.0, capital/2, 200.0)
    remaining = capital - cap_stocks

    cap_sp500 = st.number_input("S&P 500 capital", min_value = 0.0, max_value = capital/2, value = remaining/2,step=100.0)
    # cap_sp500 = st.slider("S&P 500 capital", 0.0, capital/2, remaining/2)
    remaining2 = remaining - cap_sp500
    cap_bonds = st.number_input("Bond capital", min_value = 0.0, max_value = remaining2, value = remaining2,step=100.0)
    # cap_bonds = st.slider("Bond capital", 0.0, remaining2, remaining2)

    # Descargar datos para cada activo seleccionado por el usuario
    if 'BONDS' in options:
        bonds_data = yf.download("^TNX", start=start_date, end=end_date)
    if 'SP500' in options:
        sp500_data = yf.download("^GSPC", start=start_date, end=end_date)
    if symbol in options:
        stock_data = yf.download(symbol, start=start_date, end=end_date)
        
        
    # Obtener la fecha start más tardía
    bonds_start = str(bonds_data.index.min().date())
    sp500_start = str(sp500_data.index.min().date())
    stock_start = str(stock_data.index.min().date())
    latest_start = max(bonds_start, sp500_start, stock_start)
    # Convertir la cadena de texto en formato yyyy-mm-dd a un objeto de fecha date
    latest_start = datetime.datetime.strptime(latest_start, '%Y-%m-%d').date()

    # Redeterminar start_date
    # start_date = latest_start.strftime('%Y-%m-%d')

    # Actualizar start_date si es anterior a la fecha start más tardía
    if start_date < latest_start:
        start_date = latest_start.strftime('%Y-%m-%d')
        st.write('Latest start for portfolio is',latest_start,'please adjust Start Date at sidebar')

    # Calcular la proporción de cada activo en el portafolio del usuario
    total_proportion = cap_stocks + cap_bonds + cap_sp500
    stocks_proportion = cap_stocks / total_proportion
    bonds_proportion = cap_bonds / total_proportion
    sp500_proportion = cap_sp500 / total_proportion

    # Combinar los datos de los activos en un único DataFrame
    portfolio_data = pd.DataFrame(index=stock_data.index)
    
    if 'BONDS' in options:
        price_bond = bonds_data['Close'][0] 
        amount_bonds = cap_bonds/price_bond
        amount_USD_bonds = amount_bonds * bonds_data['Close']
        portfolio_data['BONDS'] = amount_USD_bonds
    #     portfolio_data['BONDS'] = bonds_data['Close'] * bonds_proportion * capital
    if 'SP500' in options:
        price_sp500 = sp500_data['Close'][0] 
        amount_sp500 = cap_sp500/price_sp500
        amount_USD_sp500 = amount_sp500 * sp500_data['Close']
        portfolio_data['SP500'] = amount_USD_sp500
    #     portfolio_data['SP500'] = sp500_data['Close'] * sp500_proportion * capital
    if symbol in options:
        price_stock = stock_data['Close'][0] 
        amount_stocks = cap_stocks/price_stock
        amount_USD_stocks = amount_stocks * stock_data['Close']
        portfolio_data[symbol] = amount_USD_stocks
  

with col2:
    
    # Calcular el valor total del portafolio en cada fecha
    portfolio_data['Total'] = portfolio_data.sum(axis=1)
    # Crear una lista con las proporciones de cada activo en el portafolio
    proportions = [stocks_proportion, bonds_proportion, sp500_proportion]
    # Crear una lista con los nombres de los activos
    names = [symbol, "Bonds", "SP500"]
    # Crear un objeto Pie con los datos de las proporciones y nombres de activos
    pie = go.Pie(labels=names, values=proportions)
    # Crear un objeto Figure con el objeto Pie en el layout
    fig = go.Figure(pie)
    # Mostrar el gráfico en Streamlit con la función st.plotly_chart
    st.plotly_chart(fig)

performance,data = st.tabs(['KPIS','Historical Data'])

with performance:
    st.write('Portfolio KPIs')
    return_data = pd.DataFrame()
    if 'BONDS' in options:
        return_bond = bonds_data['Close'].tail(1)
        return_data['BONDS'] = return_bond
    if 'SP500' in options:
        return_sp500 = sp500_data['Close'].tail(1)
        return_data['SP500'] = return_sp500
    if symbol in options:
        return_stock = stock_data['Close'].tail(1)
        return_data[symbol] = return_stock
    return_data['Total'] = return_bond + return_sp500 + return_stock
    st.write(return_data)
    

    # calcular los retornos diarios
    retornos_diarios = portfolio_data.pct_change()

    # calcular la rentabilidad anualizada
    rentabilidad_anual = retornos_diarios.mean() * 252

    # calcular la volatilidad anualizada
    volatilidad_anual = retornos_diarios.std() * np.sqrt(252)

    # calcular la matriz de correlación de los retornos diarios
    correlacion = retornos_diarios.corr()


    # calcular la diversificación (coeficiente de Sharpe)
    rf = 0.02 # tasa libre de riesgo
    sharpe_ratio = (rentabilidad_anual - rf) / volatilidad_anual

    col1, col2, col3 = st.columns(3)
    with col1:
    # imprimir los resultados
        st.write("Annualized Return:", rentabilidad_anual)
    with col2:
        st.write("Annualized Volatility:", volatilidad_anual)
    with col3:
        st.write("Sharpe Coeficient:", sharpe_ratio)
    
    st.write("Daily Returns Correlation Matrix:", correlacion)
  
    


with data:
# Mostrar los datos del portafolio en una tabla
    st.dataframe(portfolio_data)
    if st.button('Show tail'):
            st.write(portfolio_data.tail())



