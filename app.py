import streamlit as st
import numpy as np
import pandas as pd
import requests

API_URL = "https://zoo-api-1008045770158.europe-west1.run.app/predict_tf"

st.markdown("""
    # Zoologist

    ## Make prediction !
""")

island = st.selectbox("Island", ["Biscoe", "Dream", "Torgersen"])
sex = st.selectbox("Sex", ["Male", "Female"])
bill_length_mm = st.slider(
    "Bill length (mm)",
    min_value=20.0,
    max_value=70.0,
    value=45.0,
    step=0.1
)

bill_depth_mm = st.slider(
    "Bill depth (mm)",
    min_value=10.0,
    max_value=30.0,
    value=17.0,
    step=0.1
)

flipper_length_mm = st.slider(
    "Flipper lenght (mm)",
    min_value=150.0,
    max_value=250.0,
    value=200.0,
    step=1.0
)

body_mass_g = st.slider(
    "Body mass (g)",
    min_value=2000.0,
    max_value=7000.0,
    value=4000.0,
    step=50.0
)

if st.button("Prediction", type="primary"):

    parameters = {
        "island": island,
        "bill_length_mm": bill_length_mm,
        "bill_depth_mm": bill_depth_mm,
        "flipper_length_mm": flipper_length_mm,
        "body_mass_g": body_mass_g,
        "sex": sex,
    }

    try:
        with st.spinner("Prediction in progress..."):
            response = requests.get(
                API_URL,
                params=parameters,
                timeout=30
            )

        response.raise_for_status()

        result = response.json()
        prediction = result["prediction"]

        st.success(f"Prediction : {prediction}")

    except requests.exceptions.Timeout:
        st.error("API out of time.")

    except requests.exceptions.ConnectionError:
        st.error("API error.")

    except requests.exceptions.HTTPError:
        st.error(
            f"HTTP error : {response.status_code}."
        )
        st.code(response.text)

    except KeyError:
        st.error("No prediction")
        st.json(result)

    except ValueError:
        st.error("unavable JSON.")
