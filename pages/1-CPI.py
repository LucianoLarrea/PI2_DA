import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# Carga el DataFrame CPI
CPI = pd.read_csv('./pdata/CPI_RL.csv') # usecols=fields

if st.sidebar.checkbox('Gráfico CPI',value=True):
    # st.header('CPI (Consumer Price Index)')
    # st.markdown('***')
    st.subheader('Gráfico CPI (Consumer Price Index)')

    rango_tiempo = st.slider('Definir el rango de tiempo',min_value=1960,max_value=2050,step=1,value=2022)
    X = CPI['Year']
    Y = CPI['CPI']
    fig = plt.figure(figsize=(8,6))
    sns.lineplot(x= 'Year', y = 'CPI', data=CPI[CPI['Year']<rango_tiempo])
    # fig, ax = plt.subplots()
    # ax.scatter(X[:62], Y[:62], c = 'g', s = 6)
    # plt.plot(X[62:],Y[62:], '-', c = 'b',label ='Datos proyectados')
    plt.axvline(x=2022, color='red')
    plt.xlabel('Year')
    plt.ylabel('CPI')
    plt.legend()
    st.pyplot(fig)


if st.sidebar.checkbox('Calculadora CPI'):
    # st.markdown('***')
    st.subheader('Calculadora CPI')

    
    X = CPI['Year']
    Y = CPI['CPI']
    
    col1, col2 = st.columns(2)
    with col1:
    
        Start_date = st.number_input("Año inicial 👇",min_value=1960, max_value=2050, value=2010, step=1)
        End_date = st.number_input("Año final 👇",min_value=1960, max_value=2050, value=2020, step=1)
        Valor_inicial = st.number_input("Monto inicial en USD 👇",min_value=1, max_value=10000, value=100, step=1)

        # Encontrar el índice correspondiente a start_date y final_date en el array X
        index_inicial = np.where(X == Start_date)[0][0]
        index_final = np.where(X == End_date)[0][0]

        # Asignar el correspondiente valor de Y a CPI_inicial y CPI_final
        a = 3.68164797
        b = -7189.3950

        CPI_inicial = a * X[index_inicial] + b
        CPI_final = a * X[index_final] + b

        # Calcular Valor_final
        # Valor_inicial = np.array(Valor_inicial, dtype=np.float64)
        Valor_final = Valor_inicial * CPI_inicial / CPI_final

        st.write(Valor_inicial,'USD en el año',Start_date)
        st.write(round(Valor_final,2),'USD en el año',End_date)
    
    with col2:
        image = Image.open('CPI.png')
        st.image(image, use_column_width='auto')
        DeltaTiempo = End_date-Start_date
        Diferencia = Valor_final-Valor_inicial
        Porcentaje = 100*Diferencia/Valor_inicial
        st.write('Diferencia en Años =',round(DeltaTiempo,1))
        st.write('Diferencia en USD =',round(Diferencia,1))
        st.write('Diferencia en Porcentaje = ', round(Porcentaje,1),'%')
        st.write('Porcentaje Anual =',round(Porcentaje/DeltaTiempo,1),'%')
    
    
if st.sidebar.checkbox('Tabla CPI'):
    st.markdown('***')
    st.subheader('Tabla CPI')
    
    col1, col2, col3 = st.columns(3)

    with col1:
       st.dataframe(CPI)

    with col3:
        # if st.checkbox('Vista de datos (Head o Tail)'):
        #     if st.button('Mostrar head'):
        #         st.write(CPI.head())
        if st.button('Mostrar tail'):
            st.write(CPI.tail())

    with col2:
        st.subheader('Dimensiones')

        dim = st.radio('Dimensióm a mostrar:', ('Filas', 'Columnas'),horizontal=True)
        if dim == 'Filas':
            st.write('Cantidad de filas:', CPI.shape[0])
        else:
            st.write('Cantidad de columnas:', CPI.shape[1])