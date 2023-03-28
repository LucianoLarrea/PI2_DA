import streamlit as st
import pandas as pd
import numpy as np
import time
from PIL import Image

# Crear un título para la aplicación
st.set_page_config(page_title='Investment') # Nombre para configurar la pagina web
# st.header('Data Analysis') # Titulo de la pagina

options = ['Home','Inflation', 'End']
query = st.sidebar.radio('Seleccione el tipo de consulta',options)

if query == 'Home':
        st.title('Investment asessment')
        image = Image.open('Inevitable.jpeg')
        st.image(image, caption='Thanos glove')
        st.title('My story')
        image = Image.open('PorscheFerrari.jpeg')
        st.image(image, caption='Ferrari')
        image = Image.open('PorscheMuseum.jpeg')
        st.image(image, caption='Porsche')
        image = Image.open('Mercedes.jpeg')
        st.image(image, caption='Mercedes')
        image = Image.open('Delorian.jpeg')
        st.image(image, caption='Delorian')
        image = Image.open('Porsche.jpeg')
        st.image(image, caption='The race begins')

 
        
# if query == 'CPI':
#         st.write('Welcome to CPI')

        
# if query == 'Instruments':
#         st.write('Welcome to Instruments')
       
        
if query == 'Inflation':
        col1, col2 = st.columns(2)
        with col1:
                GMS = st.number_input('Global Money Supply M1 (Trillons):',min_value=1, max_value=100, value=87, step=1)
                GAI = st.number_input('Global Anual Inflation (%):',min_value=0.5, max_value=10.5, value=3.5, step=0.1)
                rangetime = ['Half an hour','An hour','A day','A week','A month','A year']
        with col2:
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
        st.write('Loss of value over time = USD',round(LVOT,1))
        image = Image.open('Investor.jpeg')
        st.image(image, caption='Inflation glove')
                

if query == 'End':
        st.header('My investment!:sunglasses:')
        image = Image.open('Fun.jpg')
        st.image(image, caption='Suzuki Fun')
        st.markdown('''
        # Links
        - [The Growth and Composition of S&P 500](https://prod-useast-b.online.tableau.com/#/site/takticflow/views/SnP500/Dashboard1?:embed=n&:iid=1&:origin=card_share_link)
        - [All of the World’s Money and Markets](https://www.visualcapitalist.com/all-of-the-worlds-money-and-markets-in-one-visualization-2022/)
        ''', unsafe_allow_html=True)
