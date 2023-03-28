import streamlit as st
import pandas as pd
import numpy as np
import time
from PIL import Image

# Crear un título para la aplicación
st.set_page_config(page_title='Investment') # Nombre para configurar la pagina web
# st.header('Data Analysis') # Titulo de la pagina

options = ['Inicio','Conservador', 'Agresivo', 'Inflación', 'Fin']
query = st.sidebar.radio('Seleccione el tipo de consulta',options)

if query == 'Inicio':

        image = Image.open('invest.png')
        st.image(image, caption='Investment')
        st.markdown('''
        # Links
        - [The Growth and Composition of S&P 500](https://prod-useast-b.online.tableau.com/#/site/takticflow/views/SnP500/Dashboard1?:embed=n&:iid=1&:origin=card_share_link)
        - [All of the World’s Money and Markets](https://www.visualcapitalist.com/all-of-the-worlds-money-and-markets-in-one-visualization-2022/)
        ''', unsafe_allow_html=True)
 
        
if query == 'CPI':
        st.write('Bienvenido al CPI')
        st.write('Puede cambiar los parametros')
        
if query == 'Instrumentos':
        st.write('Bienvenido a Instrumentos')
        st.write('Mire que buen grafico')
        
if query == 'Inflación':
        GMS = st.number_input('Global Money Supply M1 (Trillons):',min_value=1, max_value=100, value=87, step=1)
        GAI = st.number_input('Global Anual Inflation (%):',min_value=0.5, max_value=10.5, value=3.5, step=0.1)
        rangetime = ['Half an hour','An hour','A day','A week','A month','A year']
        choose = st.radio('Select range of time:',rangetime)
        if choose == 'Half an hour':
                DIV = 0.0017520
        if choose == 'An hour':
                DIV = 0.0008760
        if choose == 'A day':
                DIV = 0.0000365
        if choose == 'A week':
                DIV = 74/14000000
        if choose == 'A month':
                DIV = 73/60000000
        if choose == 'A year':
                DIV = 1/1000000000
        LVOT = GMS * GAI / DIV
        st.write('Loss of value over time')
        st.write(LVOT)
        image = Image.open('Portafolio_de_inversiones.jpeg')
        st.image(image, caption='Portafolio_de_inversiones')
                

if query == 'Fin':
        st.header('Mi inversión!:sunglasses:')
        image = Image.open('Fun.jpg')
        st.image(image, caption='Suzuki Fun')

