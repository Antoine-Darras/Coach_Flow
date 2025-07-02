import streamlit as st
import sys
import os
import pandas as pd

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "scripts"))
)
import func_streamlit as fs
import pipeline as pl
import data_fetcher


st.markdown(
    """
    <h1 style='text-align: center; color: teal;'>
        CoachFlow 🏊 🚴 🏃 
    </h1>
    """,
    unsafe_allow_html=True,
)
st.write("---")
st.write(
    "Grâce à ton compte Garmin, tu peux suivre tes performances sportives et demander de l'aide à ton coach(flow) !"
)


EMAIL = st.text_input("Ton identifiant Garmin")
PASSWORD = st.text_input("Ton mot de passe Garmin", type="password")
st.write("---")

if st.button("Let's go !"):
    client = fs.connect_streamlit_garmin(EMAIL, PASSWORD)

    if client:
        df = pl.pipeline()
        last_activity = (
            df[["start_date", "type", "duration_hhmmss", "distance_km", "allure"]]
            .sort_values("start_date", ascending=False)
            .head(5)
            .rename(
                columns={
                    "start_date": "Date",
                    "type": "Type d'activité",
                    "duration_hhmmss": "Durée (hh:mm:ss)",
                    "distance_km": "Distance (km)",
                }
            )
        )

        st.write("---")
        st.subheader("Bravo pour tes dernières activités ! 👏💪")
        st.write(last_activity)

    else:
        st.error("La connexion a échoué. Vérifie tes identifiants.")
