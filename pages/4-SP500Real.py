import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from PIL import Image

# Carga el DataFrame SP500Real
SP500Real = pd.read_csv('./pdata/SP500Real.csv') 


if st.sidebar.checkbox('Graphic S&P 500 Real',value=True):
    # Agregar widget de radio button para seleccionar la escala del eje y
    escala = st.radio('Select scale for axis y:', ['Linear', 'Log'])
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
    plt.axvline(x=2010, color='blue')
    plt.axvline(x=2022, color='red')
    ax.axhline(y=1, color='black', linestyle='--')

    # Agregar una leyenda
    ax.legend()

    # Agregar etiquetas de los ejes y un título
    ax.set_xlabel('Year')
    ax.set_ylabel('Index')
    ax.set_title('SP500 Real')
    st.pyplot(fig)
    if st.checkbox('Interactive S&P 500 Real'):
        # Verificar la opción seleccionada por el usuario y ajustar la escala del eje y
        if escala == 'Log':
            yaxis_type = 'log'
        else:
            yaxis_type = 'linear'

        # Create traces
        fig = go.Figure()

        fig.add_trace(go.Scatter(x=SP500Real['Year'], y=SP500Real['SP500'],
                            mode='lines',
                            name='SP500 Index',
                            line=dict(color='green')))

        fig.add_trace(go.Scatter(x=SP500Real['Year'], y=SP500Real['CPI'],
                            mode='lines',
                            name='CPI',
                            line=dict(color='red')))

        fig.add_trace(go.Scatter(x=SP500Real['Year'], y=SP500Real['SP500/CPI'],
                            mode='lines',
                            name='SP500/CPI',
                            line=dict(color='blue')))

        # Add vertical shaded regions for different time periods
        fig.add_shape(type="rect",
            xref="x", yref="paper",
            x0=2000, y0=0, x1=2003, y1=1,
            fillcolor="red",
            opacity=0.3,
            layer="below"
        )

        fig.add_shape(type="rect",
            xref="x", yref="paper",
            x0=2003, y0=0, x1=2007, y1=1,
            fillcolor="green",
            opacity=0.3,
            layer="below"
        )

        fig.add_shape(type="rect",
            xref="x", yref="paper",
            x0=2007, y0=0, x1=2009, y1=1,
            fillcolor="red",
            opacity=0.3,
            layer="below"
        )

        fig.add_shape(type="rect",
            xref="x", yref="paper",
            x0=2009, y0=0, x1=2021, y1=1,
            fillcolor="green",
            opacity=0.3,
            layer="below"
        )

        fig.add_shape(type="rect",
            xref="x", yref="paper",
            x0=2021, y0=0, x1=2023, y1=1,
            fillcolor="red",
            opacity=0.3,
            layer="below"
        )

        # Set layout
        fig.update_layout(
            title="SP500 Real",
            xaxis_title="Year",
            yaxis_title="Index",
            yaxis_type=yaxis_type,
            shapes=[
                dict(
                    type='line',
                    yref='paper', y0=1, y1=1,
                    xref='x', x0=1947, x1=2023,
                    line=dict(
                        color='black',
                        dash='dash',
                    )
                )
            ],
        )
        rango_tiempo = st.slider('Definir el rango de tiempo',min_value=1960,max_value=2023,step=1,value=2000)
        # Set range of x axis based on user's input
        fig.update_xaxes(range=[rango_tiempo, 2023])

        # Display figure
        st.plotly_chart(fig)

if st.sidebar.checkbox('Calculator S&P 500 Real'):
    # st.markdown('***')
    st.subheader('Calculator S&P 500 Real')

    
    # Crear el array X de fechas
    X = SP500Real['Year']


    # Ingresar los valores de Valor_inicial, start_date y final_date
    # Valor_inicial = st.number_input("Monto inicial en USD 👇", key="viSP500", min_value=1, max_value=1000, value=100, step=1)
    col1, col2 = st.columns(2)

    with col1:
  
        Start_date = st.number_input("Start year 👇",min_value=1960, max_value=2021, value=2010, step=1)
        End_date = st.number_input("End year 👇",min_value=1960, max_value=2021, value=2020, step=1)
        Valor_inicial = st.number_input("Start Amount USD 👇",min_value=1, max_value=10000, value=100, step=1)
        
        # Encontrar el índice correspondiente a start_date y final_date en el array X
        index_inicial = np.where(X == Start_date)[0][0]
        index_final = np.where(X == End_date)[0][0]

        # Encontrar el indice correspondiente
        SP500_inicial = SP500Real['SP500/CPI'][index_inicial]
        SP500_final = SP500Real['SP500/CPI'][index_final]

        # Calcular Valor_final
        Valor_inicial = np.array(Valor_inicial)
        Valor_final = Valor_inicial * SP500_final / SP500_inicial

        st.write('USD at year',Start_date)
        st.write(round(Valor_final,1),'USD at year',End_date)
    
    with col2:
        image = Image.open('SP500Real.png')
        st.image(image, use_column_width='auto')
        DeltaTiempo = End_date-Start_date
        Diferencia = Valor_final-Valor_inicial
        Porcentaje = 100*Diferencia/Valor_inicial
        st.write('Delta years =',round(DeltaTiempo,1))
        st.write('Delta USD =',round(Diferencia,1))
        st.write('Delta Percentaje = ', round(Porcentaje,1),'%')
        st.write('Annual Percentaje=',round(Porcentaje/DeltaTiempo,1),'%')
    
if st.sidebar.checkbox('Table S&P 500 Real'):
    # st.markdown('***')
    st.subheader('Table S&P 500 Real')
    
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
        st.subheader('Dimensions')

        dim = st.radio('Dimension to show:', ('Files', 'Columns'),horizontal=True)
        if dim == 'Files':
            st.write('Files amount:', SP500Real.shape[0])
        else:
            st.write('Columns amount:', SP500Real.shape[1])