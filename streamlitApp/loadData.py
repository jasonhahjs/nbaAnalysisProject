import pandas as pd
import sqlite3

def nba_data():
    conn = sqlite3.connect("data/nba_stats.db")
    try:
        df = pd.read_sql_query("SELECT * FROM players", conn)
    finally:
        conn.close()

    # Safely calculate True Shooting %
    df["TS_PCT"] = df.apply(
        lambda row: round(row["PTS"] / (2 * (row["FGA"] + 0.44 * row["FTA"])), 3)
        if (row["FGA"] + 0.44 * row["FTA"]) > 0 else None,
        axis=1
    )

    # Safely calculate per-game statistics
    df["PTS_PER_GAME"] = (df["PTS"] / df["GP"]).round(1)
    df["REB_PER_GAME"] = (df["REB"] / df["GP"]).round(1)
    df["AST_PER_GAME"] = (df["AST"] / df["GP"]).round(1)
    df["TOV_PER_GAME"] = (df["TOV"] / df["GP"]).round(1)
    df["MIN_PER_GAME"] = (df["MIN"] / df["GP"]).round(1)

    # Round existing percentages
    if "W_PCT" in df.columns:
        df["W_PCT"] = df["W_PCT"].round(3)

    # Add readable season label
    if "SEASON_ID" in df.columns:
        df["season_display"] = df["SEASON_ID"].apply(
            lambda x: f"{str(x)[:4]}{str(x)[4:]}" if pd.notnull(x) else None
        )

    return df


# Common stat label mappings
statLabels = {
    "PTS_PER_GAME": "Points Per Game (PPG)",
    "REB_PER_GAME": "Rebounds Per Game (RPG)",
    "AST_PER_GAME": "Assists Per Game (APG)",
    "TOV_PER_GAME": "Turnovers Per Game (TOPG)",
    "MIN_PER_GAME": "Minutes Per Game (MPG)",
    "PTS": "Total Points",
    "REB": "Total Rebounds",
    "AST": "Total Assists",
    "TOV": "Total Turnovers",
    "FG_PCT": "Field Goal %",
    "TS_PCT": "True Shooting %",
    "W_PCT": "Win %",
    "PLUS_MINUS": "Plus-Minus"
}

reverseLabels = {v: k for k, v in statLabels.items()}
