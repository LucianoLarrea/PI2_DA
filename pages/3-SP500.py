import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# Carga el DataFrame SP500
SP500 = pd.read_csv('./pdata/SP500.csv') 

# st.title('S&P 500')

if st.sidebar.checkbox('Gráfico S&P 500',value=True):
    # st.markdown('***')
    # st.subheader('Gráfico S&P 500')

    # Agregar widget de radio button para seleccionar la escala del eje y
    escala = st.radio('Seleccionar escala del eje y:', ['Linear', 'Log'])
    
    rango_tiempo = st.slider('Definir el rango de tiempo',min_value=1947,max_value=2023,step=1,value=2000)
    fig = plt.figure(figsize=(8,6))
    
    # Verificar la opción seleccionada por el usuario y ajustar la escala del eje y
    if escala == 'Log':
        plt.yscale('log')
    
    sns.lineplot(x= 'Year',y=SP500['Index'], data=SP500[SP500['Year']>rango_tiempo]) # <rango_tiempo] x= 'Year', y = 'Index', x=SP500['Year'], 
    # ax.set_yscale('log')
    # Graficar el rango de fechas en rojo
    plt.axvspan(2000, 2003, color='red', alpha=0.3)

    # Graficar el rango de fechas en verde
    plt.axvspan(2003, 2007, color='green', alpha=0.3)

    # Graficar el rango de fechas en rojo
    plt.axvspan(2007, 2009, color='red', alpha=0.3)

    # Graficar el rango de fechas en verde
    plt.axvspan(2009, 2021, color='green', alpha=0.3)

    # Graficar el rango de fechas en rojo
    plt.axvspan(2021, 2023, color='red', alpha=0.3)
    plt.title('SP500')
    plt.xlabel('Year')
    plt.ylabel('Index')
    plt.legend()
    st.pyplot(fig)

if st.sidebar.checkbox('Calculadora S&P 500'):
    # st.markdown('***')
    st.subheader('Calculadora S&P 500')

    
    # Crear el array X de fechas
    X = SP500['Year']
    Y = SP500['Index']

    # Ingresar los valores de Valor_inicial, start_date y final_date
    # Valor_inicial = st.number_input("Monto inicial en USD 👇", key="viSP500", min_value=1, max_value=1000, value=100, step=1)
    col1, col2= st.columns(2)
    with col1:
        Start_date = st.number_input("Año inicial 👇",min_value=1960, max_value=2022, value=2010, step=1)
        End_date = st.number_input("Año final 👇",min_value=1960, max_value=2022, value=2020, step=1)
        Valor_inicial = st.number_input("Inicial USD 👇",min_value=1, max_value=10000, value=100, step=1)
        
        # Encontrar el índice correspondiente a start_date y final_date en el array X
        index_inicial = np.where(X == Start_date)[0][0]
        index_final = np.where(X == End_date)[0][0]

        # Encontrar el indice correspondiente
        SP500_inicial = SP500['Index'][index_inicial]
        SP500_final = SP500['Index'][index_final]

        # Calcular Valor_final
        Valor_inicial = np.array(Valor_inicial)
        Valor_final = Valor_inicial * SP500_final / SP500_inicial

        st.write('USD en el año',Start_date)
        st.write(round(Valor_final,1),'USD en el año',End_date)
        
    with col2:
        
        image = Image.open('SP500.png')
        st.image(image, use_column_width='auto')
        DeltaTiempo = End_date-Start_date
        Diferencia = Valor_final-Valor_inicial
        Porcentaje = 100*Diferencia/Valor_inicial
        st.write('Diferencia en Años =',round(DeltaTiempo,1))
        st.write('Diferencia en USD =',round(Diferencia,1))
        st.write('Diferencia en Porcentaje = ', round(Porcentaje,1),'%')
        st.write('Porcentaje Anual =',round(Porcentaje/DeltaTiempo,1),'%')
    
if st.sidebar.checkbox('Tabla S&P 500'):
    # st.markdown('***')
    st.subheader('Tabla S&P 500')
    
    col1, col2, col3 = st.columns(3)

    with col1:
       st.dataframe(SP500)

    with col3:
        # if st.checkbox('Vista de datos (Head o Tail)'):
        #     if st.button('Mostrar head'):
        #         st.write(SP500.head())
        if st.button('Mostrar tail'):
            st.write(SP500.tail())

    with col2:
        st.subheader('Dimensiones')

        dim = st.radio('Dimensióm a mostrar:', ('Filas', 'Columnas'),horizontal=True)
        if dim == 'Filas':
            st.write('Cantidad de filas:', SP500.shape[0])
        else:
            st.write('Cantidad de columnas:', SP500.shape[1])