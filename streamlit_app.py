import streamlit as st
import pandas as pd
import requests

# Функция для проверки валидности API Key
def input_api_key(api_key, city):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 401:  # Некорректный ключ
        return False, response.json()
    else:
        data_temp = response.json()
        return data_temp['main']['temp'], None
    

st.title("Анализ температуры воздуха в городах")

st.header("Загрузка исторических данных")

uploaded_file = st.file_uploader("Выберите CSV-файл с историческими данными", type=["csv"])
if uploaded_file is not None:
    # Загрузка файла
    df = pd.read_csv(uploaded_file)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    #st.dataframe(df)

    # Выбор города
    city = st.selectbox("Выберите город:", options=df['city'].unique())
    city_data = df[df['city'] == city]

    # Описательная статистика по городам
    st.write(df[df['city']==city].describe())
 

    # Ввод API Key
    with st.form("api_key_form"):
        api_key = st.text_input("Введите API Key для OpenWeatherMap", type="password")
        submitted = st.form_submit_button("Проверить")
    if submitted:
        if not api_key:
            st.error("Пожалуйста, введите API Key.")
        else:
            city_temp, error_message = input_api_key(api_key, city)
            if city_temp:
                st.success("API Key корректен!")
                #temperature_analyze(city, city_temp)
            else:
                st.error(f"Ошибка: {error_message}")


else:
    st.write("Пожалуйста, загрузите CSV-файл.")

    