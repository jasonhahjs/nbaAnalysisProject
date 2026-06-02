import pandas as pd
import sqlite3


def safe_divide(numerator, denominator, decimals=1):
    if denominator is None or denominator == 0 or pd.isna(denominator):
        return None

    return round(numerator / denominator, decimals)


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
    df["PTS_PER_GAME"] = df.apply(
        lambda row: safe_divide(row["PTS"], row["GP"], 1),
        axis=1
    )

    df["REB_PER_GAME"] = df.apply(
        lambda row: safe_divide(row["REB"], row["GP"], 1),
        axis=1
    )

    df["AST_PER_GAME"] = df.apply(
        lambda row: safe_divide(row["AST"], row["GP"], 1),
        axis=1
    )

    df["TOV_PER_GAME"] = df.apply(
        lambda row: safe_divide(row["TOV"], row["GP"], 1),
        axis=1
    )

    df["MIN_PER_GAME"] = df.apply(
        lambda row: safe_divide(row["MIN"], row["GP"], 1),
        axis=1
    )

    if "STL" in df.columns:
        df["STL_PER_GAME"] = df.apply(
            lambda row: safe_divide(row["STL"], row["GP"], 1),
            axis=1
        )
    else:
        df["STL_PER_GAME"] = None

    if "BLK" in df.columns:
        df["BLK_PER_GAME"] = df.apply(
            lambda row: safe_divide(row["BLK"], row["GP"], 1),
            axis=1
        )
    else:
        df["BLK_PER_GAME"] = None

    # Round existing percentages
    if "W_PCT" in df.columns:
        df["W_PCT"] = df["W_PCT"].round(3)

    if "FG_PCT" in df.columns:
        df["FG_PCT"] = df["FG_PCT"].round(3)

    # Basic analyst-style impact metric
    df["BASIC_IMPACT_SCORE"] = (
        df["PTS_PER_GAME"].fillna(0)
        + df["REB_PER_GAME"].fillna(0)
        + df["AST_PER_GAME"].fillna(0)
        + df["STL_PER_GAME"].fillna(0)
        + df["BLK_PER_GAME"].fillna(0)
        - df["TOV_PER_GAME"].fillna(0)
    ).round(1)

    # Scoring profile label
    df["SCORING_PROFILE"] = df["TS_PCT"].apply(
        lambda x: "High Efficiency" if pd.notnull(x) and x >= 0.600
        else "Average Efficiency" if pd.notnull(x) and x >= 0.550
        else "Low Efficiency"
    )

    # Availability score based on games played
    df["AVAILABILITY_PROFILE"] = df["GP"].apply(
        lambda x: "High Availability" if pd.notnull(x) and x >= 70
        else "Moderate Availability" if pd.notnull(x) and x >= 50
        else "Low Availability"
    )

    # Add readable season label
    if "SEASON_ID" in df.columns:
        df["season_display"] = df["SEASON_ID"].apply(
            lambda x: str(x) if pd.notnull(x) else None
        )

    return df


# Common stat label mappings
statLabels = {
    "PTS_PER_GAME": "Points Per Game (PPG)",
    "REB_PER_GAME": "Rebounds Per Game (RPG)",
    "AST_PER_GAME": "Assists Per Game (APG)",
    "TOV_PER_GAME": "Turnovers Per Game (TOPG)",
    "MIN_PER_GAME": "Minutes Per Game (MPG)",
    "STL_PER_GAME": "Steals Per Game (SPG)",
    "BLK_PER_GAME": "Blocks Per Game (BPG)",
    "BASIC_IMPACT_SCORE": "Basic Impact Score",
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