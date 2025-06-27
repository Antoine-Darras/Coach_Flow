import streamlit as st
import pandas as pd
from datetime import date
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

###########################################################################


def format_duration_hhmmss(duration):
    import pandas as pd

    if isinstance(duration, (int, float)):
        duration = pd.to_timedelta(duration, unit="s")

    total_seconds = int(duration.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


##############################################################################

# import d'un faux df pour le test
df = pd.read_csv("data/fake_activity_data.csv")
df["start_date"] = pd.to_datetime(df["start_date"])

st.set_page_config("Analyse de tes performances", "📈", "wide")
st.title("Analyse de tes performances 📈")
st.write(
    "Cette page te permet de visualiser et d'analyser tes performances sportives. Tu peux filtrer les activités par type, date et distance, et afficher des statistiques sur tes performances."
)
st.write("---")
# Charger les données


# filtres
with st.sidebar:
    st.sidebar.header("Filtres")
    show_all = st.checkbox("Toutes mes activités", value=False)

    if show_all:
        # Si la case est cochée, prendre toute la période
        start_date = df["start_date"].min().date()
        end_date = df["start_date"].max().date()
    else:
        start_date, end_date = st.date_input(
            "Choisis une plage de dates",
            value=(
                df["start_date"].min().date(),  # Convertit Timestamp en date
                date.today(),
            ),
        )

    sports = df["type"].dropna().unique().tolist()
    all_sports = st.checkbox("Tous les sports", value=True)

    if all_sports:
        # Si la case "Tous les sports" est cochée, sélectionner tous les sports
        sports_selected = sports
    else:
        sports_selected = st.multiselect(
            "Quel(s) sport(s) ?", options=sports, default=sports, key="sports_filter"
        )

df_filtered = df[
    (df["type"].isin(sports_selected))
    & (df["start_date"].dt.date >= start_date)
    & (df["start_date"].dt.date <= end_date)
]


col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Nombre d'activités")
    st.metric("Total", len(df_filtered))
with col2:
    st.subheader("Distance totale")
    total_distance = df_filtered["distance"].sum()
    st.metric("Total", f"{total_distance:.2f} km")
    st.subheader("Distance moyenne par sortie")
    avg_distance = df_filtered["distance"].mean()
    st.metric("Moyenne", f"{avg_distance:.2f} km")
with col3:
    st.subheader("Durée totale")
    total_duration = df_filtered["duration_seconds"].sum()
    total_duration_str = format_duration_hhmmss(total_duration)
    st.metric("Total", total_duration_str)

    st.subheader("Durée moyenne par sortie")
    avg_duration = df_filtered["duration_seconds"].mean()
    avg_duration_str = format_duration_hhmmss(avg_duration)
    st.metric("Moyenne", avg_duration_str)

###################################################################################################################################
# Visualisation des performances

df_weekly = (
    df_filtered.set_index("start_date")
    .resample("W")  # 'W' = weekly, fin de semaine (dimanche)
    .sum(numeric_only=True)
    .reset_index()
)
fig = px.line(
    df_weekly,
    x="start_date",
    y="distance",
    markers=True,
    title="Durée totale d'activité par semaine",
    labels={"start_date": "Semaine", "distance": "Durée (heures)"},
)

st.subheader("Distance parcourue au fil du temps")
st.plotly_chart(fig, use_container_width=True)

# Durée selon semaines ##############################################
df_weekly_duration = (
    df_filtered.set_index("start_date")
    .resample("W")
    .sum(numeric_only=True)
    .reset_index()
)
df_weekly_duration["duration_formatted"] = df_weekly_duration["duration_seconds"].map(
    format_duration_hhmmss
)
df_weekly_duration["duration_hours"] = df_weekly_duration["duration_seconds"] / 3600

fig = px.line(
    df_weekly_duration,
    x="start_date",
    y="duration_hours",
    markers=True,
    title="Durée totale d'activité par semaine",
    labels={"start_date": "Semaine", "duration_hours": "Durée (heures)"},
    hover_data={"duration_formatted": True, "duration_hours": False},
)

st.subheader("Durée d'activité au fil du temps")
st.plotly_chart(fig, use_container_width=True)
# Distance parcourue par type de sport ###############################################################
df_grouped = df_filtered.groupby("type", as_index=False).agg(
    distance=("distance", "sum")
)
df_grouped["distance_label"] = df_grouped["distance"].round(1).astype(str) + " km"

fig = px.bar(
    df_grouped,
    x="type",
    y="distance",
    title="Distance totale parcourue par type de sport",
    color="type",
    color_discrete_sequence=px.colors.qualitative.Vivid,
    labels={"type": "Type de sport", "distance": "Distance totale (km)"},
    text="distance_label",  # 👈 ici
)

fig.update_traces(textposition="outside")
fig.update_layout(
    uniformtext_minsize=8,
    uniformtext_mode="hide",
    margin=dict(t=50, b=50, l=40, r=40),
    height=600,
    width=1200,
)
st.subheader("Distance totale parcourue par type de sport")
st.plotly_chart(fig, use_container_width=True)

# Durée d'activité par type de sport ###############################################################
# 1. Formatage de la durée (optionnel, utilisé pour label hover si besoin)
df_filtered["duration_formatted"] = df_filtered["duration_seconds"].map(
    format_duration_hhmmss
)

# 2. Regroupement par type et somme des secondes
df_grouped = df_filtered.groupby("type", as_index=False).agg(
    duration_seconds=("duration_seconds", "sum")
)
df_grouped["duration_hours"] = df_grouped["duration_seconds"] / 3600


# 3. Générer labels hh:mm pour annotation
def hours_to_hhmm(hours):
    h = int(hours)
    m = int((hours - h) * 60)
    return f"{h:02d}:{m:02d}"


df_grouped["label_hhmm"] = df_grouped["duration_hours"].apply(hours_to_hhmm)

# 4. Créer le bar plot
fig = px.bar(
    df_grouped,
    x="type",
    y="duration_hours",
    labels={"duration_hours": "Durée totale (heures)", "type": "Type de sport"},
    color="type",
    color_discrete_sequence=px.colors.qualitative.Vivid,
    title="Durée totale d'activité par type de sport",
)

# 5. Ajouter les labels hh:mm au-dessus des barres
fig.update_traces(text=df_grouped["label_hhmm"], textposition="outside")


fig.update_layout(
    yaxis_title="Durée totale (heures)",
    uniformtext_minsize=8,
    uniformtext_mode="hide",
    margin=dict(t=50, b=50, l=40, r=40),
    height=600,
    width=1200,
)

st.plotly_chart(fig, use_container_width=False)
