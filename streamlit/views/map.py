import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

df = pd.read_parquet("data/processed/activities.parquet")
df_clean = df.dropna(subset=["start_latitude", "start_longitude"])

st.title("On regarde où tu fais du sport ?")

if df is None:
    st.write("Aucune activité disponible.")
else:
    st.write("Cartographie des activités")

how_many = st.number_input(
    "Indique le nombre de dernières sorties que tu veux voir",
    min_value=1,
    max_value=100,
    value=5,
    step=1,
)

st.write(f"Tu as demandé à voir {how_many} sorties.")

df_clean = df_clean.sort_values("start_date", ascending=False).head(how_many)
df_filtered = df_clean[df_clean["type"].isin(["running", "cycling"])]
df_filtered = df_filtered.sort_values("start_date", ascending=False)
last_activity = df_filtered.iloc[0]

m = folium.Map(
    location=[last_activity["start_latitude"], last_activity["start_longitude"]],
    zoom_start=7,
)

for index, row in df_clean.iterrows():
    folium.Marker(
        location=[row["start_latitude"], row["start_longitude"]],
        popup=row[["type", "start_date"]].to_string(index=False),
        icon=folium.Icon(color="blue"),
    ).add_to(m)

st_folium(m, width=1000, height=1000)
