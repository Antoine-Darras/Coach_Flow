import google.generativeai as genai
import os
import streamlit as st
import pandas as pd

df = pd.read_parquet("data/processed/activities.parquet")


genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.0-flash")

summary = [
    f"""Voici un résumé de mes 15 dernières séances :
- Types d'activités : {', '.join(df['type'].unique())}
- Distances (km) : {df['distance_km'].head(15).tolist()}
- Allures (min/km) : {df['pace_min_per_km'].round(2).head(15).tolist()}
- Durees (hh:mm:ss) : {df['duration_hhmmss'].head(15).tolist()}
- Fréquence cardiaque moyenne (bpm) : {df['avg_heart_rate'].head(15).tolist()}
- Calories brulées (kcal) : {df['calories_burned'].head(15).tolist()}
"""
]


def submit():
    user_input = st.session_state.user_prompt
    if user_input:
        # Ici tu appelles ton chatbot
        response = st.session_state.chat.send_message(user_input)
        st.session_state.history.append(("User", user_input))
        st.session_state.history.append(("CoachFlow", response.text))
        st.session_state.user_prompt = ""


if "chat" not in st.session_state:

    st.session_state.chat = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    "Tu es un coach sportif expert en course à pied et trail. Mais tu as une connaissance du triathlon. "
                    "Tu peux conseiller sur tout ce qui concerne le triathlon, y compris la nutrition, l'entraînement, les exercices de renforcement, etc."
                    " Donne des réponses claires, concrètes, bienveillantes et personnalisées, précises mais aussi courtes."
                    "Tu te bases sur les données des 15 dernières activités pour recommander la meilleure activité possible."
                    "Prends bien en compte la fréquence cardiaque moyenne par rapport à l'allure pour détermine le niveau du coureur"
                ],
            },
            {"role": "user", "parts": summary},
        ]
    )

if "history" not in st.session_state:
    st.session_state.history = []

st.markdown(
    """
    <h1 style='text-align: center; color: teal;'>
        CoachFlow 🏊 🚴 🏃 
    </h1>
    """,
    unsafe_allow_html=True,
)
st.write("---")
st.title("💬 CoachFlow - Ton coach IA personnalisé")
st.write(
    "Je te présente ton coach, ci-dessous il t'aidera à répondre à tes questions, te proposer des activités et te donner des conseils !"
)

if df is None:
    st.write("Aucune données disponibles.")
else:
    st.write("Prêt pour le coaching !")

st.write("---")
st.write("Comment ça fonctionne ?")
st.write(
    "Donne ton ou tes objectifs du moment à ton coach, il regardera tes dernières activités et te donnera des conseils personnalisés !"
)
st.write(
    "Tu peux même lui demander des conseils pour la nutrition en course ou tout ce que tu veux en rapport avec le sport !"
)
st.write("---")

user_input = st.text_input(
    "Pose une question à ton coach (ex : Quel type de séance demain ?)",
    key="user_prompt",
    on_change=submit,
)
if user_input:
    response = st.session_state.chat.send_message(user_input)
    st.session_state.history.append(("User", user_input))
    st.session_state.history.append(("CoachFlow", response.text))


for sender, message in st.session_state.history:
    if sender == "User":
        st.markdown(f"**Toi :** {message}")
    else:
        st.markdown(f"**CoachFlow :** {message}")
