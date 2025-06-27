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
        st.success("Connexion réussie à Garmin !")
        df_activities = pl.pipeline(client)

        df_clean = df_activities.data_fetcher.clean_basics(df_activities)
        last_activity = df_clean.sort_values("start_date", ascending=False).iloc[0]

        st.write("---")
        st.subheader("Bravo pour ta dernière activité ! 👏💪")
        st.write(last_activity)

    else:
        st.error("La connexion a échoué. Vérifie tes identifiants.")
