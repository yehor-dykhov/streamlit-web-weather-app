import time
import streamlit as st
import plotly.express as px

from api import get_weather_data

if 'weather_days_data' not in st.session_state:
    st.session_state.weather_days_data = {}


def handle_city_change():
    weather_data = get_weather_data(st.session_state["city"])

    if len(weather_data) == 0:
        st.session_state.weather_days_data = {}

    for item in weather_data:
        date_simple_str = time.strftime('%Y-%m-%d', time.gmtime(item['dt']))
        transformed_data = {
            'dt': item['dt'],
            'dt_txt': item['dt_txt'],
            'temp': item['main']['temp'],
            'feels_like': item['main']['feels_like']
        }

        if date_simple_str in st.session_state["weather_days_data"]:
            st.session_state.weather_days_data[date_simple_str].append(transformed_data)
        else:
            st.session_state.weather_days_data[date_simple_str] = [transformed_data]


def get_fig_data(days, type_data):
    value_by_type = 'temp' if type_data == 'Temperature' else 'feels_like'
    weather_days_keys = list(st.session_state.weather_days_data.keys())[:days]
    weather_days_values_by_day = [st.session_state.weather_days_data[day_date] for day_date in weather_days_keys]
    weather_days_values = []

    for day in weather_days_values_by_day:
        weather_days_values = weather_days_values + day

    dates = [date_str['dt_txt'] for date_str in weather_days_values]
    temperatures = [date_str[value_by_type] for date_str in weather_days_values]

    return dates, temperatures


st.title('Weather Forecast for the Next Days')

st.text_input('City', key='city', on_change=handle_city_change, )
st.slider('Forecast Days', key='days', min_value=1, max_value=6, help='Select the number of forecasted days')
st.selectbox('Type of data to view', key='data_type', options=['Temperature', 'Feels like'])

if st.session_state["city"] and len(list(st.session_state.weather_days_data.keys())) > 0:
    st.subheader(
        f'{st.session_state["data_type"]} '
        f'for the next {st.session_state["days"]} '
        f'day{"s" if st.session_state["days"] > 1 else ""} '
        f'in {st.session_state["city"]}'
    )

    dates, temperatures = get_fig_data(st.session_state.days, st.session_state.data_type)

    fig = px.line(x=dates, y=temperatures, labels={'x': 'Dates', 'y': 'Temperatures (C)'})
    st.plotly_chart(fig)
else:
    st.subheader(f'No data for {st.session_state["city"] or "____"} city')
