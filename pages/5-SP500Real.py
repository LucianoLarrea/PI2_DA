import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# Carga el DataFrame SP500Real
SP500Real = pd.read_csv('./data/SP500Real.csv') 


if st.sidebar.checkbox('Gráfico S&P 500 Real',value=True):
    # Agregar widget de radio button para seleccionar la escala del eje y
    escala = st.radio('Seleccionar escala del eje y:', ['Linear', 'Log'])
    # if st.checkbox('Escala Logaritmica'):
    #     escala = 'log'
    # else: escala = 'linear'
    fig, ax = plt.subplots()
    # Graficar la serie de tiempo completa
    
    # Verificar la opción seleccionada por el usuario y ajustar la escala del eje y
    if escala == 'Log':
        plt.yscale('log')
    ax.plot(SP500Real['Year'],SP500Real['CPI'], label='CPI', color='red')
    ax.plot(SP500Real['Year'],SP500Real['SP500'], label='SP500 Index', color='green')
    ax.plot(SP500Real['Year'],SP500Real['SP500/CPI'], label='SP500/CPI', color='blue')
    
    # Graficar el rango de fechas en verde
    plt.axvspan(1960, 1974, color='green', alpha=0.3)

    # Graficar el rango de fechas en rojo
    plt.axvspan(1974, 1985, color='red', alpha=0.3)

    # Graficar el rango de fechas en verde
    plt.axvspan(1985, 2021, color='green', alpha=0.3)
    # # Configurar la escala logarítmica en el eje Y
    # ax.set_yscale(escala)
    ax.axhline(y=1, color='black', linestyle='--')

    # Agregar una leyenda
    ax.legend()

    # Agregar etiquetas de los ejes y un título
    ax.set_xlabel('Year')
    ax.set_ylabel('Index')
    ax.set_title('SP500 Real')
    st.pyplot(fig)

if st.sidebar.checkbox('Calculadora S&P 500 Real'):
    # st.markdown('***')
    st.subheader('Calculadora S&P 500 Real')

    
    # Crear el array X de fechas
    X = SP500Real['Year']


    # Ingresar los valores de Valor_inicial, start_date y final_date
    # Valor_inicial = st.number_input("Monto inicial en USD 👇", key="viSP500", min_value=1, max_value=1000, value=100, step=1)
    col1, col2 = st.columns(2)

    with col1:
  
        Start_date = st.number_input("Año inicio 👇",min_value=1960, max_value=2021, value=2010, step=1)
        End_date = st.number_input("Año fin 👇",min_value=1960, max_value=2021, value=2020, step=1)
        Valor_inicial = st.number_input("USD Inicial 👇",min_value=1, max_value=10000, value=100, step=1)
        
        # Encontrar el índice correspondiente a start_date y final_date en el array X
        index_inicial = np.where(X == Start_date)[0][0]
        index_final = np.where(X == End_date)[0][0]

        # Encontrar el indice correspondiente
        SP500_inicial = SP500Real['SP500/CPI'][index_inicial]
        SP500_final = SP500Real['SP500/CPI'][index_final]

        # Calcular Valor_final
        Valor_inicial = np.array(Valor_inicial)
        Valor_final = Valor_inicial * SP500_final / SP500_inicial

        st.write('USD en el año',Start_date)
        st.write(round(Valor_final,1),'USD en el año',End_date)
    
    with col2:
        image = Image.open('SP500Real.png')
        st.image(image, use_column_width='auto')
        DeltaTiempo = End_date-Start_date
        Diferencia = Valor_final-Valor_inicial
        Porcentaje = 100*Diferencia/Valor_inicial
        st.write('Diferencia en Años =',round(DeltaTiempo,1))
        st.write('Diferencia en USD =',round(Diferencia,1))
        st.write('Diferencia en Porcentaje = ', round(Porcentaje,1),'%')
        st.write('Porcentaje Anual =',round(Porcentaje/DeltaTiempo,1),'%')
    
if st.sidebar.checkbox('Tabla S&P 500 Real'):
    # st.markdown('***')
    st.subheader('Tabla S&P 500 Real')
    
    col1, col2, col3 = st.columns(3)

    with col1:
       st.dataframe(SP500Real)

    with col3:
        # if st.checkbox('Vista de datos (Head o Tail)'):
        #     if st.button('Mostrar head'):
        #         st.write(SP500Real.head())
        if st.button('Mostrar tail'):
            st.write(SP500Real.tail())

    with col2:
        st.subheader('Dimensiones')

        dim = st.radio('Dimensióm a mostrar:', ('Filas', 'Columnas'),horizontal=True)
        if dim == 'Filas':
            st.write('Cantidad de filas:', SP500Real.shape[0])
        else:
            st.write('Cantidad de columnas:', SP500Real.shape[1])