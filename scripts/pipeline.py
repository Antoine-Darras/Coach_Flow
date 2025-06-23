import pandas as pd
import garmin_connect as gc
import data_fetcher
import os
import duckdb
from dotenv import load_dotenv


def pipeline():
    df = data_fetcher.activity_basics()
    os.makedirs("data/processed", exist_ok=True)
    con = duckdb.connect("data/processed/coachflow.duckdb")
    con.execute("CREATE OR REPLACE TABLE activities AS SELECT * FROM df")
    df.to_csv("data/processed/activities.csv", index=False)
    return df


if __name__ == "__main__":
    df = pipeline()
    if df is not None:
        print("Pipeline complet exécuté avec succès.")
        print(df.head())
    else:
        print("Erreur dans la pipeline.")
