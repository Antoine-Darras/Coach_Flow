import pandas as pd
import garmin_connect as gc
import data_fetcher
import os
import duckdb
from dotenv import load_dotenv


def pipeline():
    df = data_fetcher.get_and_clean_activities()
    df.to_parquet("data/processed/activities.parquet")
    return df


if __name__ == "__main__":
    try:
        df = pipeline()
        if df is not None:
            print("Pipeline complet exécuté avec succès.")
            print(df.head())
        else:
            print("Erreur dans la pipeline.")
    except Exception as e:
        print("Une erreur est survenue lors de l’exécution de la pipeline :")
        print(e)
