import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
from PIL import Image

# Carga el DataFrame GS10
GS10 = pd.read_csv('pdata/GS10.csv',index_col=0) # 
DFII10 = pd.read_csv('pdata/DFII10.csv',index_col=0)
DFII10CS = pd.read_csv('pdata/DFII10CS.csv',index_col=0)
st.title('Bonos del Tesoro')

GS10.index = pd.to_datetime(GS10.index,format='%Y-%m-%d')
# GS10['Date'] =  pd.to_datetime(GS10['Date'],format='%Y-%m-%d')
# GS10.set_index(GS10['Date'])

if st.sidebar.checkbox('Gráfico Bonos del Tesoro',value=True):
    # Agregar widget de radio button para seleccionar la escala del eje y
    # escala = st.radio('Seleccionar escala del eje y:', ['Linear', 'Log'])
    
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
    plt.plot(GS10F['GS10'], label='Bonos del Tesoro', color='blue') # ,data=GS10.index>rango_tiempo
    plt.ylabel('Percent')
    plt.title('Bonos del Tesoro')
    ax.legend()

    st.pyplot(fig)

if st.sidebar.checkbox('Gráfico Bonos del Tesoro Ajustados'):

    # escala = st.radio('Seleccionar escala del eje y:', ['Linear', 'Log'])
    fig, ax = plt.subplots()
    # if escala == 'Log':
    #     plt.yscale('log')
    DFII10.index = pd.to_datetime(DFII10.index,format='%Y-%m-%d')
    # rango_tiempo = st.slider('Definir el rango de tiempo',min_value=1960,max_value=2023,step=1,value=2000)
    plt.plot(DFII10['DFII10'], label='Adjusted Treasuries Bonds', color='blue') # ,data=DFII10.index>rango_tiempo
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
    plt.title('Adjusted Treasuries Bonds')
    ax.axhline(y=0, color='black', linestyle='--')
    ax.legend()

    st.pyplot(fig)
    
    # st.line_chart(DFII10['DFII10'])
    
if st.sidebar.checkbox('Gráfico Bonos Acumulados'):

    # escala = st.radio('Seleccionar escala del eje y:', ['Linear', 'Log'])
    fig, ax = plt.subplots()
    # if escala == 'Log':
    #     plt.yscale('log')
    DFII10.index = pd.to_datetime(DFII10.index,format='%Y-%m-%d')
    # rango_tiempo = st.slider('Definir el rango de tiempo',min_value=1960,max_value=2023,step=1,value=2000)
    plt.plot(DFII10CS['DFCumSum'], label='Adjusted CumSum Bonds', color='blue') # ,data=DFII10.index>rango_tiempo

    plt.ylabel('Cumuled Percent')
    plt.title('Adjusted CumSum Bonds')
    ax.axhline(y=0, color='black', linestyle='--')
    ax.legend()

    st.pyplot(fig)
    
    
if st.sidebar.checkbox('Calculadora Bonos'):
    # st.markdown('***')
    st.subheader('Calculadora Bonos')

    
    X = DFII10CS.index
    Y = DFII10CS['DFCumSum']
    
    col1, col2 = st.columns(2)
    with col1:
    
        Start_date = st.number_input("Año inicial 👇",min_value=2003, max_value=2023, value=2010, step=1)
        End_date = st.number_input("Año final 👇",min_value=2003, max_value=2023, value=2020, step=1)
        Valor_inicial = st.number_input("Monto inicial en USD 👇",min_value=1, max_value=10000, value=100, step=1)

        Bonos_inicial = DFII10CS['DFCumSum'][Start_date]
        Bonos_final = DFII10CS['DFCumSum'][End_date]
        Valor_final = Valor_inicial * (1+((Bonos_final - Bonos_inicial) / 100))

        st.write(Valor_inicial,'USD en el año',Start_date)
        st.write(round(Valor_final,2),'USD en el año',End_date)
    
    with col2:
        image = Image.open('Adjusted CumSum Bonds.png')
        st.image(image, use_column_width='auto')
        DeltaTiempo = End_date-Start_date
        Diferencia = Valor_final-Valor_inicial
        Porcentaje = 100*Diferencia/Valor_inicial
        st.write('Diferencia en Años =',round(DeltaTiempo,1))
        st.write('Diferencia en USD =',round(Diferencia,1))
        st.write('Diferencia en Porcentaje = ', round(Porcentaje,1),'%')
        st.write('Porcentaje Anual =',round(Porcentaje/DeltaTiempo,1),'%')    

if st.sidebar.checkbox('Tabla Bonos del Tesoro'):
    st.markdown('***')
    st.subheader('Tabla Bonos del Tesoro')
    
    col1, col2, col3 = st.columns(3)

    with col1:
       st.dataframe(GS10)

    with col3:
        # if st.checkbox('Vista de datos (Head o Tail)'):
        #     if st.button('Mostrar head'):
        #         st.write(GS10.head())
        if st.button('Mostrar tail'):
            st.write(GS10.tail())

    with col2:
        st.subheader('Dimensiones')

        dim = st.radio('Dimensióm a mostrar:', ('Filas', 'Columnas'),horizontal=True)
        if dim == 'Filas':
            st.write('Cantidad de filas:', GS10.shape[0])
        else:
            st.write('Cantidad de columnas:', GS10.shape[1])
    
if st.sidebar.checkbox('Tabla Bonos del Tesoro Ajustados'):
    # st.markdown('***')
    st.subheader('Tabla Bonos del Tesoro Ajustados')
    
    col1, col2, col3 = st.columns(3)

    with col1:
       st.dataframe(DFII10)

    with col3:
        if st.button('Mostrar tail'):
            st.write(DFII10.tail())

    with col2:
        st.subheader('Dimensiones')

        dim = st.radio('Dimensióm a mostrar:', ('Filas', 'Columnas'),horizontal=True)
        if dim == 'Filas':
            st.write('Cantidad de filas:', DFII10.shape[0])
        else:
            st.write('Cantidad de columnas:', DFII10.shape[1])
