import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import plotly.graph_objs as go
import datetime as dt
from PIL import Image
import yfinance as yf

# Carga el DataFrame GS10
GS10 = pd.read_csv('pdata/GS10.csv',index_col=0) # 
DFII10 = pd.read_csv('pdata/DFII10.csv',index_col=0)
DFII10CS = pd.read_csv('pdata/DFII10CS.csv',index_col=0)
st.title('US Treasury Bonds')

GS10.index = pd.to_datetime(GS10.index,format='%Y-%m-%d')
# GS10['Date'] =  pd.to_datetime(GS10['Date'],format='%Y-%m-%d')
# GS10.set_index(GS10['Date'])

# Definir los símbolos de los activos a analizar
symbol_cpi = 'CPIAUCSL' # Índice de precios al consumidor
symbol_treasury_bonds = '^TNX' # Bono del Tesoro de EE. UU. a 10 años

# Correlacion entre Bonds y CPI
# Obtener los datos históricos de los precios de cierre de ambos activos
df_cpi = yf.download(symbol_cpi, start='2010-01-01', end='2023-03-29', interval='1mo')['Adj Close']
df_treasury_bonds = yf.download(symbol_treasury_bonds, start='2010-01-01', end='2023-03-29', interval='1mo')['Adj Close']
# Concatenar ambos dataframes en uno solo
df = pd.concat([df_cpi, df_treasury_bonds], axis=1)
df.columns = ['CPI', '10 years treasury bond']
#Calcular el coeficiente de correlación entre los dos activos
correlation = df.corr().iloc[0,1]


if st.sidebar.checkbox('Graphic Bonds',value=True):

    
    fecha_inicio = pd.to_datetime("2003-01-02")
    # # fecha_fin = pd.to_datetime("2022-01-04")
    # df_filtrado = GS10.loc[(GS10.index >= fecha_inicio)] # & (df["fecha"] <= fecha_fin)]
    # st.line_chart(df_filtrado["GS10"])

    fig, ax = plt.subplots()
    # if escala == 'Log':
    #     plt.yscale('log')
    # GS10.index = pd.to_datetime(GS10.index,format='%Y-%m-%d')
    # rango_tiempo = st.slider('Definir el rango de tiempo',min_value=1960,max_value=2023,step=1,value=2000)
    GS10F = GS10.loc[(GS10.index >= fecha_inicio)]
    plt.plot(GS10F['GS10'], label='Bonds', color='blue') # ,data=GS10.index>rango_tiempo
    plt.axvline(x=14865, color='blue')
    plt.axvline(x=19000, color='red')
    plt.ylabel('Percent')
    plt.title('Bonds')
    ax.legend()
    st.pyplot(fig)
    if st.checkbox('Interactive Bonds'):
        # Crear la figura
        fig = go.Figure()

        # Agregar la línea
        GS10F = GS10.loc[(GS10.index >= fecha_inicio)]
        fig.add_trace(go.Scatter(x=GS10F.index, y=GS10F['GS10'], mode='lines', name='Bonds', line=dict(color='blue')))

        # Personalizar el diseño y la presentación
        fig.update_layout(title='Bonds',
                        xaxis_title='Date',
                        yaxis_title='Percentaje',
                        font=dict(family='Arial, sans-serif', size=12, color='black'),
                        hovermode='x unified')

        # Mostrar la figura
        fig.show()
    # st.write('Correlation between the CPI and the 10-year Treasury bond:', correlation)

if st.sidebar.checkbox('Graphic Adjusted Bonds'):

    # escala = st.radio('Seleccionar escala del eje y:', ['Linear', 'Log'])
    fig, ax = plt.subplots()
    # if escala == 'Log':
    #     plt.yscale('log')
    DFII10.index = pd.to_datetime(DFII10.index,format='%Y-%m-%d')
    # rango_tiempo = st.slider('Definir el rango de tiempo',min_value=1960,max_value=2023,step=1,value=2000)
    plt.plot(DFII10['DFII10'], label='Adjusted Treasurie Bonds', color='blue') # ,data=DFII10.index>rango_tiempo
    # plt.axvspan(2003-01-02, 2011-03-30, color='green', alpha=0.3)
    # Definir fechas de inicio y fin del rango
    start1 = pd.to_datetime('2003-01-02',format='%Y-%m-%d')
    end1 = pd.to_datetime('2011-11-03',format='%Y-%m-%d')
    plt.axvspan(start1, end1, color='green', alpha=0.3)
    
    start2 = pd.to_datetime('2011-11-03',format='%Y-%m-%d')
    end2 = pd.to_datetime('2013-06-07',format='%Y-%m-%d')
    plt.axvspan(start2, end2, color='red', alpha=0.3)
    
    start3 = pd.to_datetime('2013-06-07',format='%Y-%m-%d')
    end3 = pd.to_datetime('2020-03-23',format='%Y-%m-%d')
    plt.axvspan(start3, end3, color='green', alpha=0.3)
    
    start4 = pd.to_datetime('2020-03-23',format='%Y-%m-%d')
    end4 = pd.to_datetime('2022-04-29',format='%Y-%m-%d')
    plt.axvspan(start4, end4, color='red', alpha=0.3)
    
    start5 = pd.to_datetime('2022-04-29',format='%Y-%m-%d')
    end5 = pd.to_datetime('2023-03-23',format='%Y-%m-%d')
    plt.axvspan(start5, end5, color='green', alpha=0.3)
    
    plt.ylabel('Percent')
    plt.title('Adjusted Treasurie Bonds')
    ax.axhline(y=0, color='black', linestyle='--')
    ax.legend()

    st.pyplot(fig)
    
    # st.line_chart(DFII10['DFII10'])
    
    if st.checkbox('Interactive Adjusted Bonds'):
        DFII10.index = pd.to_datetime(DFII10.index, format='%Y-%m-%d')
        # rango_tiempo = st.slider('Definir el rango de tiempo', min_value=1960, max_value=2023, step=1, value=2000)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=DFII10.index, y=DFII10['DFII10'], mode='lines', name='Adjusted Treasurie Bonds', line=dict(color='blue')))

        # Definir fechas de inicio y fin del rango
        start1 = pd.to_datetime('2003-01-02', format='%Y-%m-%d')
        end1 = pd.to_datetime('2011-11-03', format='%Y-%m-%d')
        fig.add_shape(type="rect", x0=start1, y0=-0.1, x1=end1, y1=0.1, line=dict(color='green', width=0), fillcolor='green', opacity=0.3)

        start2 = pd.to_datetime('2011-11-03', format='%Y-%m-%d')
        end2 = pd.to_datetime('2013-06-07', format='%Y-%m-%d')
        fig.add_shape(type="rect", x0=start2, y0=-0.1, x1=end2, y1=0.1, line=dict(color='red', width=0), fillcolor='red', opacity=0.3)

        start3 = pd.to_datetime('2013-06-07', format='%Y-%m-%d')
        end3 = pd.to_datetime('2020-03-23', format='%Y-%m-%d')
        fig.add_shape(type="rect", x0=start3, y0=-0.1, x1=end3, y1=0.1, line=dict(color='green', width=0), fillcolor='green', opacity=0.3)

        start4 = pd.to_datetime('2020-03-23', format='%Y-%m-%d')
        end4 = pd.to_datetime('2022-04-29', format='%Y-%m-%d')
        fig.add_shape(type="rect", x0=start4, y0=-0.1, x1=end4, y1=0.1, line=dict(color='red', width=0), fillcolor='red', opacity=0.3)

        start5 = pd.to_datetime('2022-04-29', format='%Y-%m-%d')
        end5 = pd.to_datetime('2023-03-23', format='%Y-%m-%d')
        fig.add_shape(type="rect", x0=start5, y0=-0.1, x1=end5, y1=0.1, line=dict(color='green', width=0), fillcolor='green', opacity=0.3)

        fig.update_yaxes(title='Percent')
        fig.update_layout(title='Adjusted Treasurie Bonds', xaxis=dict(title='Date'))
        st.plotly_chart(fig)
    
if st.sidebar.checkbox('Graphic Accumulated Bonds'):

    # escala = st.radio('Seleccionar escala del eje y:', ['Linear', 'Log'])
    fig, ax = plt.subplots()
    # if escala == 'Log':
    #     plt.yscale('log')
    DFII10.index = pd.to_datetime(DFII10.index,format='%Y-%m-%d')
    # rango_tiempo = st.slider('Definir el rango de tiempo',min_value=1960,max_value=2023,step=1,value=2000)
    plt.plot(DFII10CS['DFCumSum'], label='Adjusted Accumulated Bonds', color='blue') # ,data=DFII10.index>rango_tiempo

    plt.ylabel('Accumulated Percent')
    plt.title('Adjusted Accumulated Bonds')
    ax.axhline(y=0, color='black', linestyle='--')
    ax.legend()
    st.pyplot(fig)
    if st.checkbox('Interactive Adjusted Accumulated Bonds'):
        st.line_chart(DFII10CS['DFCumSum'])
    
if st.sidebar.checkbox('Calculator Bonds'):
    # st.markdown('***')
    st.subheader('Calculator Bonds')

    
    X = DFII10CS.index
    Y = DFII10CS['DFCumSum']
    
    col1, col2 = st.columns(2)
    with col1:
    
        Start_date = st.number_input("Start year 👇",min_value=2003, max_value=2023, value=2010, step=1)
        End_date = st.number_input("End year 👇",min_value=2003, max_value=2023, value=2020, step=1)
        Valor_inicial = st.number_input("Initial amount USD 👇",min_value=1, max_value=10000, value=100, step=1)

        Bonos_inicial = DFII10CS['DFCumSum'][Start_date]
        Bonos_final = DFII10CS['DFCumSum'][End_date]
        Valor_final = Valor_inicial * (1+((Bonos_final - Bonos_inicial) / 100))

        st.write(Valor_inicial,'USD at year',Start_date)
        st.write(round(Valor_final,2),'USD at year',End_date)
    
    with col2:
        image = Image.open('Adjusted CumSum Bonds.png')
        st.image(image, use_column_width='auto')
        DeltaTiempo = End_date-Start_date
        Diferencia = Valor_final-Valor_inicial
        Porcentaje = 100*Diferencia/Valor_inicial
        st.write('Delta years =',round(DeltaTiempo,1))
        st.write('Delta USD =',round(Diferencia,1))
        st.write('Delta Percentaje = ', round(Porcentaje,1),'%')
        st.write('Annual Percentaje=',round(Porcentaje/DeltaTiempo,1),'%')    

if st.sidebar.checkbox('Table Bonds'):
    st.markdown('***')
    st.subheader('Table Bonds')
    
    col1, col2, col3 = st.columns(3)

    with col1:
       st.dataframe(GS10)

    with col3:
        # if st.checkbox('Vista de datos (Head o Tail)'):
        #     if st.button('Mostrar head'):
        #         st.write(GS10.head())
        if st.button('Show tail'):
            st.write(GS10.tail())

    with col2:
        st.subheader('Dimensions')

        dim = st.radio('Dimension to show:', ('Files', 'Columns'),horizontal=True)
        if dim == 'Files':
            st.write('Files amount:', GS10.shape[0])
        else:
            st.write('Columns amount:', GS10.shape[1])
    
if st.sidebar.checkbox('Table Adjusted Bonds'):
    # st.markdown('***')
    st.subheader('Table Adjusted Bonds')
    
    col1, col2, col3 = st.columns(3)

    with col1:
       st.dataframe(DFII10)

    with col3:
        if st.button('Show tail'):
            st.write(DFII10.tail())

    with col2:
        st.subheader('Dimensions')

        dim = st.radio('Dimension to show:', ('Files', 'Columns'),horizontal=True)
        if dim == 'Files':
            st.write('Files amount:', DFII10.shape[0])
        else:
            st.write('Columns amount:', DFII10.shape[1])
