import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import plotly.graph_objs as go

# Carga el DataFrame CPI
CPI = pd.read_csv('./pdata/CPI_RL.csv') # usecols=fields

if st.sidebar.checkbox('Graphic CPI',value=True):
    # st.header('CPI (Consumer Price Index)')
    # st.markdown('***')
    st.subheader('Graphic CPI (Consumer Price Index)')

    rango_tiempo = st.slider('Define range time',min_value=1960,max_value=2040,step=1,value=2010)
    X = CPI['Year']
    Y = CPI['CPI']
    fig = plt.figure(figsize=(8,6))
    sns.lineplot(x= 'Year', y = 'CPI', data=CPI[CPI['Year']<rango_tiempo])
    # fig, ax = plt.subplots()
    plt.scatter(X[:62], Y[:62], c = 'g', s = 6)
    # plt.plot(X[62:],Y[62:], '-', c = 'b',label ='Datos proyectados')
    plt.axvline(x=2010, color='blue')
    plt.axvline(x=2022, color='red')
    plt.xlabel('Year')
    plt.ylabel('CPI')
    plt.legend()
    st.pyplot(fig)
    if st.checkbox('Interactive CPI',value=False):
    # Grafico de plolty
        fig = go.Figure()

        # Agregar la línea
        fig.add_trace(go.Scatter(x=CPI['Year'], y=CPI['CPI'], mode='lines', name='CPI'))

        # Agregar los puntos
        fig.add_trace(go.Scatter(x=CPI['Year'][:62], y=CPI['CPI'][:62], mode='markers', name='Datos históricos'))
        fig.add_trace(go.Scatter(x=CPI['Year'][62:], y=CPI['CPI'][62:], mode='lines', name='Datos proyectados'))

        # Agregar la línea vertical
        fig.add_shape(dict(type='line', x0=2022, y0=0, x1=2022, y1=300, line=dict(color='red', width=2)))

        # Personalizar el diseño y la presentación
        fig.update_layout(title='Consumer Price Index (CPI)',
                        xaxis_title='Year',
                        yaxis_title='Consumer Price Index',
                        font=dict(family='Arial, sans-serif', size=12, color='black'),
                        hovermode='x unified')

# Mostrar la figura
fig.show()


if st.sidebar.checkbox('Calculator CPI'):
    # st.markdown('***')
    st.subheader('Calculator CPI')

    
    X = CPI['Year']
    Y = CPI['CPI']
    
    col1, col2 = st.columns(2)
    with col1:
    
        Start_date = st.number_input("Start year 👇",min_value=1960, max_value=2050, value=2010, step=1)
        End_date = st.number_input("End year👇",min_value=1960, max_value=2050, value=2020, step=1)
        Valor_inicial = st.number_input("Start Amount USD 👇",min_value=1, max_value=10000, value=100, step=1)

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

        st.write(Valor_inicial,'USD at year',Start_date)
        st.write(round(Valor_final,2),'USD at year',End_date)
    
    with col2:
        image = Image.open('CPI.png')
        st.image(image, use_column_width='auto')
        DeltaTiempo = End_date-Start_date
        Diferencia = Valor_final-Valor_inicial
        Porcentaje = 100*Diferencia/Valor_inicial
        st.write('Delta years =',round(DeltaTiempo,1))
        st.write('Delta USD =',round(Diferencia,1))
        st.write('Delta Percentaje = ', round(Porcentaje,1),'%')
        st.write('Annual Percentaje=',round(Porcentaje/DeltaTiempo,1),'%')
    
    
if st.sidebar.checkbox('Table CPI'):
    st.markdown('***')
    st.subheader('Table CPI')
    
    col1, col2, col3 = st.columns(3)

    with col1:
       st.dataframe(CPI)

    with col3:

        if st.button('Show tail'):
            st.write(CPI.tail())

    with col2:
        st.subheader('Dimensions')

        dim = st.radio('Dimension to show:', ('Files', 'Columns'),horizontal=True)
        if dim == 'Files':
            st.write('Files Amount:', CPI.shape[0])
        else:
            st.write('Columns Amount:', CPI.shape[1])