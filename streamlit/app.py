import streamlit as st

# **Page Config**
accueil = st.Page(page="views/home.py", title="Accueil", icon="👟", default=True)

perf = st.Page(page="views/performance.py", title="Analyse des performances", icon="📈")

coach = st.Page(
    page="views/recommandation.py", title="Les conseils du coach", icon="🧑‍🏫"
)

map = st.Page(page="views/map.py", title="Cartographie des activités", icon="🗺️")

# **Navigation setup**


pg = st.navigation(pages=[accueil, perf, coach, map])

pg.run()
