import streamlit as st
import numpy as np
import pandas as pd

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
