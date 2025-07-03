# 🧠 CoachFlow – Analyse & Recommandation Sportive Personnalisée

CoachFlow est une application interactive développée en Python avec Streamlit. Elle permet d'analyser automatiquement vos activités sportives issues de Garmin Connect et de recevoir des recommandations personnalisées basées sur vos données récentes.

> 🔒 Aucune donnée d'identification n'est stockée : la connexion à Garmin se fait via une API sécurisée, uniquement pendant la session.

---

## 🚀 Fonctionnalités

- 📥 Importation automatique des activités Garmin
- 🧹 Nettoyage & enrichissement des données (distance, vitesse, durée, type…)
- 🗺️ Carte interactive centrée sur votre dernière activité (via Folium)
- 📈 Tableau de bord de vos dernières activités (via Plotly)
- 🧠 Page "Les conseils du coach" : chatbot IA (via Gemini) avec recommandations personnalisées

---

## 🛠️ Stack technique

- `Python` – Traitement des données
- `Streamlit` – Interface web interactive
- `Folium` – Cartographie interactive
- `Pandas` – Manipulation des données
- `Plotly` – Visualisations dynamiques
- `uv` – Gestionnaire de paquets moderne
- `pyproject.toml` – Déclaration des dépendances
- `garminconnect` – Connexion à Garmin Connect
- `Google Gemini` – IA conversationnelle (via API)

---


## 📂 Structure du projet


```
Coach_Flow/
│
├── data/ # Données brutes et nettoyées
│ └── processed/
├── garmin/ # Connexion et récupération Garmin
│ └── client.py
├── pipeline/ # Traitements de données
│ └── processing.py
├── streamlit/
│ ├── app.py # Point d'entrée Streamlit
│ └── views/
│ ├── home.py
│ ├── map.py
│ └── recommandation.py
├── utils/ # Fonctions utilitaires
├── assets/ # Logos, images, etc.
├── .streamlit/
│ └── secrets.example.toml # Exemple de configuration sécurisée
├── pyproject.toml # Dépendances (via uv)
├── uv.lock # Versions verrouillées
└── README.md
```

## 🔐 Configuration requise

Certaines fonctionnalités (comme le chatbot IA) nécessitent une clé API Gemini.

Rendez-vous sur Google AI Studio (https://makersuite.google.com/app/apikey) pour créer une clé API Gemini.

Copiez cette clé dans un fichier .streamlit/secrets.toml :

```
# .streamlit/secrets.toml
gemini_api_key = "votre_clé_API_Gemini"
```
💡 Un exemple de structure vous est fourni dans .streamlit/secrets.example.toml.

⚠️ Ne partagez jamais votre secrets.toml. Il est volontairement ignoré dans .gitignore pour éviter toute fuite de données sensibles.

## ⚙️ Installation
1. Clonez le repo :
```
git clone https://github.com/Antoine-Darras/Coach_Flow.git
cd Coach_Flow
```
2. Créez et activez un environnement virtuel :
```
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate           # Windows
```

3. Installez les dépendances avec uv :
```
uv sync
```
4. Lancez l'application :
```
streamlit run streamlit/app.py
```