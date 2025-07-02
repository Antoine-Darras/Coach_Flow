🧠 CoachFlow – Analyse & Recommandation Sportive Personnalisée
CoachFlow est une application interactive développée en Python avec Streamlit. Elle permet d'analyser automatiquement vos activités sportives issues de Garmin et de recevoir des recommandations personnalisées basées sur vos données récentes.

## 🚀 Fonctionnalités

📥 Importation automatique des activités Garmin
🧹 Nettoyage & enrichissement des données (distance, vitesse, durée, type…)
🗺️ Carte interactive (Folium) centrée sur votre dernière activité
🧠 Page "Les conseils du coach" : IA et recommandations (en cours)
📈 Tableau de bord de vos dernières activités
🔐 Authentification utilisateur (à venir)


## 🛠️ Stack technique

Python
Streamlit – Interface utilisateur
Folium – Cartographie interactive
Pandas – Traitement des données
Plotly – Visualisations dynamiques
uv – Gestionnaire de paquets moderne
pyproject.toml – Configuration des dépendances
Garmin Connect

## 📂 Structure du projet


```
Coach_Flow/
│
├── data/                        # Données brutes et nettoyées
│   └── processed/
├── garmin/                      # Connexion et récupération Garmin
│   └── client.py
├── pipeline/                    # Traitements de données (cleaning, enrichissement…)
│   └── processing.py
├── streamlit/
│   ├── app.py                   # Point d'entrée Streamlit
│   └── views/                   # Pages de l'app
│       ├── home.py
│       ├── map.py
│       └── recommandation.py
├── utils/                       # Fonctions utilitaires
├── assets/                      # Logos, captures, etc.
├── pyproject.toml               # Configuration des dépendances (gérée avec uv)
├── uv.lock                      # Verrouillage des versions
└── README.md
```

## ⚙️ Installation
1. Clonez le repo :
git clone https://github.com/Antoine-Darras/Coach_Flow.git
cd Coach_Flow

2. Créez et activez un environnement virtuel :
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate           # Windows

3. Installez les dépendances avec uv :
uv sync

4. Lancez l'application :
streamlit run streamlit/app.py