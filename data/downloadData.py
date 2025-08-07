import os
import time
import sqlite3
import pandas as pd
from datetime import datetime
from nba_api.stats.endpoints import leaguedashplayerstats
import requests

def get_all_season_ids(start=1996):
    today = datetime.today()
    current_year = today.year
    current_month = today.month

    if current_month >= 7:
        end_year = current_year
    else:
        end_year = current_year - 1

    season_ids = []
    for year in range(start, end_year):
        start_yr = str(year)[-2:]
        end_yr = str(year + 1)[-2:]
        season_ids.append(f"{year}-{end_yr}")

    return season_ids

def get_existing_seasons(conn):
    try:
        query = "SELECT DISTINCT SEASON_ID FROM players"
        existing_df = pd.read_sql(query, conn)
        return set(existing_df["SEASON_ID"].unique())
    except Exception:
        return set()

def fetch_season_data(season, max_retries=3):
    valid_nba_team_ids = {
        1610612737, 1610612738, 1610612739, 1610612740, 1610612741,
        1610612742, 1610612743, 1610612744, 1610612745, 1610612746,
        1610612747, 1610612748, 1610612749, 1610612750, 1610612751,
        1610612752, 1610612753, 1610612754, 1610612755, 1610612756,
        1610612757, 1610612758, 1610612759, 1610612760, 1610612761,
        1610612762, 1610612763, 1610612764, 1610612765, 1610612766
    }

    for attempt in range(max_retries):
        try:
            print(f"Fetching {season}... (Attempt {attempt + 1})")
            stats = leaguedashplayerstats.LeagueDashPlayerStats(season=season)
            df = stats.get_data_frames()[0]

            # Filter to valid NBA team IDs
            if "TEAM_ID" in df.columns:
                df = df[df["TEAM_ID"].isin(valid_nba_team_ids)]

            # Filter out players with fewer than 20 games played
            if "GP" in df.columns:
                df = df[df["GP"] >= 20]

            return df
        except Exception as e:
            print(f"Failed to fetch {season} on attempt {attempt + 1}: {e}")
            time.sleep(2)
    print(f"Skipping {season} after {max_retries} failed attempts.")
    return None

def download_and_store_data():
    print("Preparing to download player stats...")

    db_path = "data/nba_stats.db"
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(db_path)

    try:
        season_ids = get_all_season_ids()
        existing_seasons = get_existing_seasons(conn)
        missing_seasons = [s for s in season_ids if s not in existing_seasons]

        # Step 1: Create the table if it doesn't exist
        table_check = pd.read_sql(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='players';", conn
        )
        table_exists = not table_check.empty

        if not table_exists and missing_seasons:
            first_season = missing_seasons.pop(0)
            df = fetch_season_data(first_season)
            if df is not None:
                df["SEASON_ID"] = first_season
                df.to_sql("players", conn, index=False, if_exists="replace")
                print(f"Created 'players' table using {first_season}")
                time.sleep(1.5)

        # Step 2: Process all remaining seasons
        for season in missing_seasons:
            print(f"Checking {season}")
            df = fetch_season_data(season)
            if df is None:
                continue

            df["SEASON_ID"] = season

            # Align to existing table schema
            existing_cols = pd.read_sql("PRAGMA table_info(players);", conn)["name"].tolist()

            unexpected_cols = [col for col in df.columns if col not in existing_cols]
            missing_cols = [col for col in existing_cols if col not in df.columns]

            if unexpected_cols or missing_cols:
                print(f"Schema adjustment for {season}:")
                if unexpected_cols:
                    print(f" - Dropping unexpected columns: {unexpected_cols}")
                if missing_cols:
                    print(f" - Filling missing columns with None: {missing_cols}")

            # Fill missing columns with None
            for col in missing_cols:
                df[col] = None

            # Drop extra columns
            df = df[[col for col in existing_cols if col in df.columns]]

            # Reorder and insert
            df = df[existing_cols]
            df.to_sql("players", conn, index=False, if_exists="append")
            time.sleep(1.5)

    finally:
        conn.close()

    print("Download complete.")

if __name__ == "__main__":
    download_and_store_data()
