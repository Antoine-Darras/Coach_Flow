import os
from dotenv import load_dotenv
from garminconnect import Garmin
from garminconnect import GarminConnectConnectionError

load_dotenv()  # Load environment variables from .env file


def connect_to_garmin():
    """
    Fonction principale qui établit la connexion au compte Garmin Connect
    en utilisant les identifiants stockés dans les variables d’environnement.

    Elle gère les erreurs d’authentification, de connexion réseau et
    autres erreurs inattendues pour garantir une exécution propre du script.

    Si la connexion est réussie, un message de confirmation est affiché.
    """
    EMAIL = os.getenv("GARMIN_EMAIL")
    PASSWORD = os.getenv("GARMIN_PASSWORD")

    try:
        client = Garmin(EMAIL, PASSWORD)
        client.login()
        print("Connexion réussie à Garmin Connect.")

    except GarminConnectConnectionError:
        print(
            "Erreur de connexion à Garmin Connect. Veuillez vérifier votre connexion Internet et réessayer."
        )
    except Exception as e:
        print(f"Une erreur inattendue s'est produite : {e}")
        return


if __name__ == "__main__":
    connect_to_garmin()  # Exécute la fonction de connexion si le script est exécuté directement
    # Si le script est importé, la fonction ne sera pas exécutée automatiquement
    # Cela permet de garder le code modulaire et réutilisable dans d'autres scripts.
