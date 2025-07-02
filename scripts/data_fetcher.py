import pandas as pd
import garmin_connect as gc
import numpy as np
import math


def convert_seconds_to_hhmmss(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"


def safe_format_pace(x):
    # On logue les valeurs problématiques
    if x is None or pd.isna(x) or math.isinf(x) or x <= 0:
        print(f"Valeur pace_min_per_km problématique détectée : {x}")
        return None
    try:
        minutes = int(x)
        seconds = int(round((x - minutes) * 60))
        if seconds == 60:
            minutes += 1
            seconds = 0
        return f"{minutes}:{seconds:02d} min/km"
    except Exception as e:
        print(f"Erreur inattendue sur pace {x}: {e}")
        return None


def format_pace(pace_float):
    try:
        if (
            pace_float is None
            or pd.isna(pace_float)
            or np.isinf(pace_float)
            or pace_float <= 0
        ):
            return None
        minutes = int(pace_float)
        seconds = int(round((pace_float - minutes) * 60))
        if seconds == 60:
            minutes += 1
            seconds = 0
        return f"{minutes}:{seconds:02d} min/km"
    except Exception as e:
        print(f"[format_pace] Erreur sur valeur {pace_float}: {e}")
        return None


def clean_basics(df):
    df["type"] = df["type"].apply(
        lambda x: x.get("typeKey") if isinstance(x, dict) else x
    )

    # Distance en km, arrondi correct
    df["distance_km"] = (df["distance_meters"] / 1000).round(2)

    df["duration_hhmmss"] = df["duration_seconds"].apply(convert_seconds_to_hhmmss)
    df["speed_kmh"] = round(df["avg_speed_mps"] * 3.6, 2)
    df["duration_min"] = df["duration_seconds"] / 60

    min_distance_km = 0.001  # Seuil pour éviter division par zéro
    df["pace_min_per_km"] = np.where(
        df["distance_km"] >= min_distance_km,
        df["duration_min"] / df["distance_km"],
        np.nan,
    )
    df["pace_min_per_km"] = pd.to_numeric(df["pace_min_per_km"], errors="coerce")
    df.loc[np.isinf(df["pace_min_per_km"]), "pace_min_per_km"] = np.nan
    print("Valeurs infinies restantes :")
    print(df[df["pace_min_per_km"] == np.inf])
    df["allure"] = df["pace_min_per_km"].apply(format_pace)
    df["pace_min_per_km"] = pd.to_numeric(df["pace_min_per_km"], errors="coerce")
    df.loc[np.isinf(df["pace_min_per_km"]), "pace_min_per_km"] = np.nan

    print("Valeurs infinies après calcul pace_min_per_km :")
    print(
        df.loc[
            np.isinf(df["pace_min_per_km"]),
            ["distance_km", "duration_min", "pace_min_per_km"],
        ]
    )

    df["start_time"] = pd.to_datetime(df["start_time"])
    df["start_date"] = df["start_time"].dt.date
    df["start_time"] = df["start_time"].dt.time

    return df


def get_and_clean_activities():
    client = gc.connect_to_garmin()
    if client is None:
        raise ValueError("Connexion à Garmin Connect échouée.")
    activities = client.get_activities(0, 1000)
    data = []
    for activity in activities:
        data.append(
            {
                "activityId": activity.get("activityId"),
                "activityName": activity.get("activityName"),
                "activityType": activity.get("activityType"),
                "distance": activity.get("distance"),
                "duration": activity.get("duration"),
                "averageSpeed": activity.get("averageSpeed"),
                "startTimeLocal": activity.get("startTimeLocal"),
                "calories": activity.get("calories"),
                "startLatitude": activity.get("startLatitude"),
                "startLongitude": activity.get("startLongitude"),
                "elevationGain": activity.get("elevationGain"),
                "elevationLoss": activity.get("elevationLoss"),
                "averageHR": activity.get("averageHR"),
                "maxHR": activity.get("maxHR"),
            }
        )

    df = pd.DataFrame(data)

    rename_map = {
        "activityId": "id",
        "activityName": "name",
        "activityType": "type",
        "distance": "distance_meters",
        "duration": "duration_seconds",
        "averageSpeed": "avg_speed_mps",
        "startTimeLocal": "start_time",
        "startLatitude": "start_latitude",
        "startLongitude": "start_longitude",
        "elevationGain": "elevation_gain",
        "elevationLoss": "elevation_loss",
        "averageHR": "avg_heart_rate",
        "maxHR": "max_heart_rate",
    }

    # Si la colonne "calories" existe dans df, on l'ajoute au renommage
    if "calories" in df.columns:
        rename_map["calories"] = "calories_burned"

    df = df.rename(columns=rename_map)

    # Convertir les colonnes numériques au bon type
    numeric_cols = [
        "distance_meters",
        "duration_seconds",
        "avg_speed_mps",
        "calories_burned" if "calories_burned" in df.columns else None,
        "start_latitude",
        "start_longitude",
        "elevation_gain",
        "elevation_loss",
        "avg_heart_rate",
        "max_heart_rate",
    ]
    numeric_cols = [col for col in numeric_cols if col is not None]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df.sort_values(by="start_time", ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)

    df = clean_basics(df)

    return df


if __name__ == "__main__":
    df = get_and_clean_activities()
    if df is not None and not df.empty:
        print("Activités récupérées avec succès.")
        print(df.head())
        print(df.info())
        print(df["start_time"].min(), df["start_time"].max())
    else:
        print("Aucune activité récupérée.")
