from garminconnect import Garmin
from garminconnect import GarminConnectConnectionError
import streamlit as st


def connect_streamlit_garmin(EMAIL=None, PASSWORD=None):

    try:
        client = Garmin(EMAIL, PASSWORD)
        client.login()
        st.success("Connexion réussie à Garmin Connect.")
        return client  # Retourne le client connecté pour une utilisation ultérieure

    except GarminConnectConnectionError:
        st.error(
            "Erreur de connexion à Garmin Connect. Veuillez vérifier votre connexion Internet et réessayer."
        )
    except Exception as e:
        st.error(f"Une erreur inattendue s'est produite : {e}")
        return client


if __name__ == "__main__":
    connect_streamlit_garmin()  # Exécute la fonction de connexion si le script est exécuté directement
    # Si le script est importé, la fonction ne sera pas exécutée automatiquement
    # Cela permet de garder le code modulaire et réutilisable dans d'autres scripts.
