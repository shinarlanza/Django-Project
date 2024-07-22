import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import altair as alt
import pandas as pd
import requests

st.title("Analytics Dashboard")
st.write("v.0.0.1")

swapi_endpoint = 'https://swapi.dev/api/people/1/'
api_url = 'http://127.0.0.1:8000/api/customers/'

# -- FUNCTIONS --
def fetch_data(endpoint):
    response = requests.get(endpoint)
    data = response.json()
    return data

def sent_data(name, gender, age, favorite_number):
    gender_value = "0" if gender == "Female" else "1"
    data = {
        "name": name,
        "gender": gender_value,
        "age": age,
        "favorite_number": favorite_number
    }

    respnse = requests.post(api_url, json=data)
    return respnse

# -- LAYOUT --
col1, col2 = st.columns(2)

with col1:
    st.header('Column 1')
    st.write()

    with st.expander("click something"):
        st.write('options to choose something')
        st.write('options to choose something1')
        st.write('options to choose something2')

with col2:
    # -- TEST CHART --
    categories = ['A', 'B', 'C', 'D']
    values = np.random.randint(10, 100, size=(4,))

    fig, ax = plt.subplots()
    ax.bar(categories, values, color='blue')
    ax.set_xlabel('categories')
    ax.set_ylabel('values')
    ax.set_title('Bar Chart')
    st.pyplot(fig)

# -- SESSION STATE --
if 'counter' not in st.session_state:
    st.session_state.counter = 0

if st.button('increment'):
    st.session_state.counter += 1

st.write(f"Counter value : {st.session_state.counter}")


# -- DATA FROM SWAPI API --

swapi_data = fetch_data(swapi_endpoint)
st.write('Data from the SWAPI API')
st.json(swapi_data)


# -- FETCH data from the API --

data = fetch_data(api_url)

if data:
    df = pd.DataFrame(data)

    st.dataframe(df)

    scatter_plot = alt.Chart(df).mark_circle().encode(
        x = 'age',
        y = 'favorite_number'
    )

    st.altair_chart(scatter_plot, use_container_width = True)

# -- FORM TO COLLECT DATA --
name = st.text_input("Name")
gender = st.radio("Gender", ["Male", "Female"])
age = st.slider("Age",1,100,18)
favorite_number = st.number_input("Fave Number", step=1)

if st.button("Submit"):
    response = sent_data(name, gender, age, favorite_number)
    if response.status_code == 201:
        st.success("New customer data created.")
        st.rerun()
    else:
        st.error("Something went wrong.")
