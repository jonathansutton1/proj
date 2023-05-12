import requests
import pandas as pd
import streamlit as st
import base64
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from io import BytesIO


st.set_page_config(page_title='Consulta de jogos de futebol', page_icon=':soccer:', layout='wide')
st.title("Consulta de jogos de futebol")
st.subheader("Desenvolvido por: Gabriel Guindi")

key = '17c23233af794906bb7808bc775ee4f9'
competition = st.selectbox('Escolha a competição:', ['UEFA Champions League', 'UEFA Europa League', 'Copa do Mundo'])
date = st.date_input('Escolha a data:')

if competition == 'UEFA Champions League':
    url = f'https://api.sportsdata.io/v4/soccer/stats/json/BoxScoresByDate/UCL/{date}?key={key}'
elif competition == 'UEFA Europa League':
    url = f'https://api.sportsdata.io/v4/soccer/stats/json/BoxScoresByDate/UEL/{date}?key={key}'
else:
    url = f'https://api.sportsdata.io/v4/soccer/stats/json/BoxScoresByDate/FIFA/{date}?key={key}'

def get_csv_penaltis(url):
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    tabel1 = driver.find_element('tag name', 'pre').text
    driver.quit()

    df = json.loads(tabel1)
    try:
        df1 = pd.DataFrame(df[0]['PenaltyShootouts'])
        df1.drop(columns=['GameId','PlayerId','Position'], axis=1, inplace=True)
        st.write(df1)
        csv_data = df1.to_csv(index=False)
        return csv_data
    except IndexError:
        st.warning("Não há dados disponíveis para a data especificada.")
        return None
    
    
    
if st.button('Pesquisar'):
    csv_data = get_csv_penaltis(url)
    if csv_data is not None:
        st.download_button('Download CSV', csv_data, file_name='data.csv', mime='text/csv')
else:
    pass

# Personaliza o layout da página
st.markdown('<style>body { background-color: #F5F5F5; }</style>', unsafe_allow_html=True)


