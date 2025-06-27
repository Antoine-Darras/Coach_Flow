import pandas as pd
import garmin_connect as gc


def avg_speed_mps_to_pace_min_per_km(speed_mps):
    """
    Convertit une vitesse en m/s en allure min/km.
    Renvoie une chaîne 'mm:ss' ou None si vitesse nulle, None ou NaN.
    """
    if speed_mps is None or pd.isna(speed_mps) or speed_mps == 0:
        return None

    speed_kmh = speed_mps * 3.6
    total_minutes = 60 / speed_kmh
    minutes = int(total_minutes)
    seconds = int(round((total_minutes - minutes) * 60))
    return f"{minutes:02d}:{seconds:02d}"


def convert_seconds_to_hhmmss(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"


def clean_basics(df):
    df["type"] = df["type"].apply(
        lambda x: x.get("typeKey") if isinstance(x, dict) else x
    )
    df["distance"] = round(df["distance_meters"] / 1000, 2)
    df["duration_hhmmss"] = df["duration_seconds"].apply(convert_seconds_to_hhmmss)
    df["speed_kmh"] = round(df["avg_speed_mps"] * 3.6, 2)
    df["start_time"] = pd.to_datetime(df["start_time"])
    df["start_date"] = df["start_time"].dt.date
    df["start_time"] = df["start_time"].dt.time
    df["allure"] = df["avg_speed_mps"].apply(avg_speed_mps_to_pace_min_per_km)
    return df


def activity_basics(client):
    client = (
        gc.connect_to_garmin()
    )  # Connect to Garmin Connect using the function from garmin_connect.py
    activities = client.get_activities(0, 1000)
    data = []  # Initialize an empty list to store activity data
    for activity in activities:
        data.append(
            {
                "activityId": activity["activityId"],
                "activityName": activity["activityName"],
                "activityType": activity["activityType"],
                "distance": activity.get("distance"),
                "duration": activity["duration"],
                "averageSpeed": activity.get("averageSpeed"),
                "startTimeLocal": activity["startTimeLocal"],
                "calories": activity.get("calories"),
                "startLatitude": activity.get("startLatitude"),
                "startLongitude": activity.get("startLongitude"),
                "elevationGain": activity.get("elevationGain"),
                "elevationLoss": activity.get("elevationLoss"),
                "averageHR": activity.get("averageHR"),
                "maxHR": activity.get("maxHR"),
            }
        )

    df = pd.DataFrame(data)  # Convert the list of dictionaries to a DataFrame
    df = df.rename(
        columns={
            "activityId": "id",
            "activityName": "name",
            "activityType": "type",
            "distance": "distance_meters",
            "duration": "duration_seconds",
            "averageSpeed": "avg_speed_mps",
            "startTimeLocal": "start_time",
            "calories": "calories_burned" if "calories" in data[0] else None,
            "startLatitude": "start_latitude",
            "startLongitude": "start_longitude",
            "elevationGain": "elevation_gain",
            "elevationLoss": "elevation_loss",
            "averageHR": "avg_heart_rate",
            "maxHR": "max_heart_rate",
        }
    )
    df.sort_values(
        by="start_time", ascending=False, inplace=True
    )  # Sort by start time in descending order
    df.reset_index(drop=True, inplace=True)  # Reset the index of the DataFrame
    df = clean_basics(df)
    return df  # Return the cleaned DataFrame with activity basics


if (
    __name__ == "__main__"
):  # If this script is run directly, execute the activity_basics function
    df = activity_basics()  # Call the function to fetch activity data
    if df is not None:
        print("Activités récupérées avec succès.")
        print(df.head())  # Affiche les 5 premières lignes du DataFrame
        print(df.info())  # Affiche les informations du DataFrame
        print(
            df["start_time"].min(), df["start_time"].max()
        )  # Affiche la date min et max

    else:
        print("Aucune activité récupérée.")
