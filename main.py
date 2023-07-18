import streamlit as st


def handle_city_change():
    print(f'LOL: {st.session_state["city"]}')


st.title('Weather Forecast for the Next Days')

st.text_input('City', key='city', on_change=handle_city_change, )
st.slider('Forecast Days', key='days', min_value=1, max_value=5, help='Select the number of forecasted days')
st.selectbox('Type of data to view', key='data_type', options=['Temperature', 'Sky'])

if st.session_state["city"]:
    st.subheader(
        f'{st.session_state["data_type"]} '
        f'for the next {st.session_state["days"]} '
        f'day{"s" if st.session_state["days"] > 1 else ""} '
        f'in {st.session_state["city"]}'
    )

    st.bar_chart()
