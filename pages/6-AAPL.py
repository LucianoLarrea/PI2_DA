import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# Carga el DataFrame PF1
PF1 = pd.read_csv('./pdata/PF1.csv') 
# PF1 = PF1.set_index('Year',inplace=True)
# st.title('Portfolio SP500 + Apple')



if st.sidebar.checkbox('Gráfico SP500 + Apple',value=True):
    # Agregar widget de radio button para seleccionar la escala del eje y
    escala = st.radio('Seleccionar escala del eje y:', ['Linear', 'Log'])
    options = st.multiselect('Seleccionar índices:',['SP500', 'Apple', 'CPI', 'Portfolio'], [ 'Apple', 'Portfolio'])

    
    # if st.checkbox('Escala Logaritmica'):
    #     escala = 'log'
    # else: escala = 'linear'
    fig, ax = plt.subplots()
    # Graficar la serie de tiempo completa
    
    # Verificar la opción seleccionada por el usuario y ajustar la escala del eje y
    if escala == 'Log':
        plt.yscale('log')
    if 'SP500' in options:
        plt.plot(PF1['Year'], PF1['SP80'], label='SP500', color='blue')
    if 'Apple' in options:
        plt.plot(PF1['Year'], PF1['IdxAAPL'], label='Apple', color='green')
    if 'Portfolio' in options:
        plt.plot(PF1['Year'], PF1['Portfolio'], label='Portfolio', color='red')
    if 'CPI' in options:
        plt.plot(PF1['Year'], PF1['CPI80'], label='CPI', color='red')



    # # Graficar el rango de fechas en verde
    # plt.axvspan(1960, 1973, color='green', alpha=0.3)

    # # Graficar el rango de fechas en rojo
    # plt.axvspan(1973, 1985, color='red', alpha=0.3)

    # # Graficar el rango de fechas en verde
    # plt.axvspan(1985, 2021, color='green', alpha=0.3)
    # # Configurar la escala logarítmica en el eje Y
    # ax.set_yscale(escala)


    # Agregar una leyenda
    ax.legend()

    # Agregar etiquetas de los ejes y un título
    ax.set_xlabel('Year')
    ax.set_ylabel('Price')
    ax.set_title('Portfolio SP500 + Apple')
    st.pyplot(fig)


if st.sidebar.checkbox('Calculadora SP500 + Apple'):
    # st.markdown('***')
    st.subheader('Calculadora SP500 + Apple')
  
    # Crear el array X de fechas
    X = PF1['Year']
    col1, col2 = st.columns(2)

    with col1:
        Start_date = st.number_input("Año inicio 👇",min_value=1960, max_value=2021, value=2010, step=1)
        End_date = st.number_input("Año fin 👇",min_value=1960, max_value=2021, value=2020, step=1)
        Valor_inicial = st.number_input("USD Inicial 👇",min_value=1, max_value=10000, value=100, step=1)
        
        # Encontrar el índice correspondiente a start_date y final_date en el array X
        index_inicial = np.where(X == Start_date)[0][0]
        index_final = np.where(X == End_date)[0][0]

        # Encontrar el indice correspondiente
        SP500_inicial = PF1['Portfolio'][index_inicial]
        SP500_final = PF1['Portfolio'][index_final]

        # Calcular Valor_final
        Valor_inicial = np.array(Valor_inicial)
        Valor_final = Valor_inicial * SP500_final / SP500_inicial

        st.write('USD en el año',Start_date)
        st.write(Valor_final,'USD en el año',End_date)
        
    with col2:
        image = Image.open('Apple.png')
        st.image(image, use_column_width='auto')
        DeltaTiempo = End_date-Start_date
        Diferencia = Valor_final-Valor_inicial
        Porcentaje = 100*Diferencia/Valor_inicial
        st.write('Diferencia en Años =',round(DeltaTiempo,1))
        st.write('Diferencia en USD =',round(Diferencia,1))
        st.write('Diferencia en Porcentaje = ', round(Porcentaje,1),'%')
        st.write('Porcentaje Anual =',round(Porcentaje/DeltaTiempo,1),'%')
    
if st.sidebar.checkbox('Tabla SP500 + Apple'):
    # st.markdown('***')
    st.subheader('Tabla SP500 + Apple')
    
    col1, col2, col3 = st.columns(3)

    with col1:
       st.dataframe(PF1)

    with col3:
        # if st.checkbox('Vista de datos (Head o Tail)'):
        #     if st.button('Mostrar head'):
        #         st.write(PF1.head())
        if st.button('Mostrar tail'):
            st.write(PF1.tail())

    with col2:
        st.subheader('Dimensiones')

        dim = st.radio('Dimensióm a mostrar:', ('Filas', 'Columnas'),horizontal=True)
        if dim == 'Filas':
            st.write('Cantidad de filas:', PF1.shape[0])
        else:
            st.write('Cantidad de columnas:', PF1.shape[1])