import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Definir los símbolos de los activos a analizar
symbol_sp500 = '^GSPC' # S&P 500
symbol_treasury_bonds = '^TNX' # Bono del Tesoro de EE. UU. a 10 años

# Obtener los datos históricos de los precios de cierre de ambos activos
df_sp500 = yf.download(symbol_sp500, start='2010-01-01', end='2023-03-29', interval='1d')['Adj Close']
df_treasury_bonds = yf.download(symbol_treasury_bonds, start='2010-01-01', end='2023-03-29', interval='1d')['Adj Close']

# Concatenar ambos dataframes en uno solo
df = pd.concat([df_sp500, df_treasury_bonds], axis=1)
df.columns = ['S&P 500', '10 years treasury bond']

# Calcular el coeficiente de correlación entre los dos activos
correlation = df.corr().iloc[0,1]

st.sidebar.checkbox('Graphic S&P 500 + Bonos',value=True)

fig, ax = plt.subplots()

ax.plot(df_sp500.index,df_sp500, label='SP500', color='green')
# crear un segundo eje y para los datos de bonos del tesoro
ax2 = ax.twinx()
ax2.plot(df_treasury_bonds.index,df_treasury_bonds, label='Bond', color='blue')

# Agregar una leyenda
ax.legend(loc='upper left')
ax2.legend(loc='upper right')

# Agregar etiquetas de los ejes y un título
ax.set_xlabel('Year')
ax.set_ylabel('Index')
ax.set_title('SP500 Real')
st.pyplot(fig)
if st.checkbox('Interactive S&P 500 + Bonds'):
    # Crear una figura con dos ejes Y
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Agregar la serie de datos del SP500 al primer eje Y
    fig.add_trace(
        go.Scatter(x=df_sp500.index, y=df_sp500, name='SP500', line=dict(color='green')),
        secondary_y=False)

    # Agregar la serie de datos de bonos del tesoro al segundo eje Y
    fig.add_trace(
        go.Scatter(x=df_treasury_bonds.index, y=df_treasury_bonds, name='Bond', line=dict(color='blue')),
        secondary_y=True)

    # Agregar etiquetas de los ejes y un título
    fig.update_xaxes(title_text="Year")
    fig.update_yaxes(title_text="SP500", secondary_y=False)
    fig.update_yaxes(title_text="Bond", secondary_y=True)
    fig.update_layout(title="SP500 Real")

    # Mostrar la figura
    st.plotly_chart(fig)

# Mostrar los resultados en Streamlit
st.write('Historical correlation between the S&P 500 and the 10-year Treasury bond:', correlation)
st.markdown("""---""")
# Calcular los retornos diarios para ambos activos
# returns = df.pct_change()

# Calcular el retorno del portafolio conformado en partes iguales por el S&P 500 y los bonos del Tesoro
# portfolio_returns = returns.mean(axis=1)

# Mostrar los resultados en Streamlit
# st.write('Historical returns of the equally-weighted portfolio of the S&P 500 and the 10-year Treasury bond:', portfolio_returns)


    