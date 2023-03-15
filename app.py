import pandas as pd
import streamlit as st
from dbhelper import DB
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

db = DB()
st.sidebar.title("Flight Analytics")

user_option = st.sidebar.selectbox('Menu', ['Select One', 'Check Flights', 'Analytics'])

if user_option == 'Check Flights':

    col1, col2 = st.columns(2)
    city = db.fetch_city_names()

    with col1:
        Source = st.selectbox('Source', sorted(city))
    with col2:
        Destination = st.selectbox('Destination', sorted(city))
    if st.button('Search'):
        results = db.fetch_all_flights(Source, Destination)
        df = pd.DataFrame(results)
        df = df.rename(columns={0: 'Airlines', 1: 'Route', 2: 'Departure', 3: 'Duration',4:'Price'})
        st.table(df)

elif user_option == 'Analytics':

    airline, frequency = db.fetch_airline_frequency()
    fig = go.Figure(
        go.Pie(
            labels=airline,
            values=frequency,
            hoverinfo="label+percent",
            textinfo="value"
        ))

    st.header("Pie chart")
    st.plotly_chart(fig)

    city, frequency1 = db.busy_airport()
    fig = px.bar(
        x=city,
        y=frequency1
    )

    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    date, frequency2 = db.daily_frequency()
    fig = px.line(
        x=date,
        y=frequency2
    )

    st.plotly_chart(fig, theme="streamlit", use_container_width=True)


else:
    st.title('Tell me  about')
