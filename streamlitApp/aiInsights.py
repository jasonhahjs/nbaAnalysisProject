import os
from pathlib import Path

from openai import OpenAI
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

MISSING_API_KEY_MESSAGE = (
    "OPENAI_API_KEY is not set. Add it to a .env file in the project root "
    "(the same folder as setup.py) using OPENAI_API_KEY=your_key_here, "
    "or add it to Streamlit secrets."
)


def format_player_context(player_row):
    return f"""
Player Name: {player_row.get("PLAYER_NAME")}
Team: {player_row.get("TEAM_ABBREVIATION")}
Season: {player_row.get("season_display")}
Games Played: {player_row.get("GP")}
Minutes Per Game: {player_row.get("MIN_PER_GAME")}
Points Per Game: {player_row.get("PTS_PER_GAME")}
Rebounds Per Game: {player_row.get("REB_PER_GAME")}
Assists Per Game: {player_row.get("AST_PER_GAME")}
Turnovers Per Game: {player_row.get("TOV_PER_GAME")}
Steals Per Game: {player_row.get("STL_PER_GAME")}
Blocks Per Game: {player_row.get("BLK_PER_GAME")}
True Shooting Percentage: {player_row.get("TS_PCT")}
Field Goal Percentage: {player_row.get("FG_PCT")}
Win Percentage: {player_row.get("W_PCT")}
Plus-Minus: {player_row.get("PLUS_MINUS")}
Basic Impact Score: {player_row.get("BASIC_IMPACT_SCORE")}
Scoring Profile: {player_row.get("SCORING_PROFILE")}
Availability Profile: {player_row.get("AVAILABILITY_PROFILE")}
"""


def format_top_players_context(top_df, selected_stat_label):
    rows = []

    for index, row in top_df.iterrows():
        rows.append(
            f"""
Player: {row.get("PLAYER_NAME")}
Team: {row.get("TEAM_ABBREVIATION")}
Season: {row.get("season_display")}
Games Played: {row.get("GP")}
Points Per Game: {row.get("PTS_PER_GAME")}
Rebounds Per Game: {row.get("REB_PER_GAME")}
Assists Per Game: {row.get("AST_PER_GAME")}
True Shooting Percentage: {row.get("TS_PCT")}
Basic Impact Score: {row.get("BASIC_IMPACT_SCORE")}
Selected Ranking Stat: {selected_stat_label}
"""
        )

    return "\n".join(rows)


def get_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY") or get_streamlit_secret("OPENAI_API_KEY")

    if not api_key:
        return None

    return OpenAI(api_key=api_key)


def get_streamlit_secret(secret_name):
    try:
        import streamlit as st

        return st.secrets.get(secret_name)
    except Exception:
        return None


def generate_player_summary(player_row):
    client = get_openai_client()

    if client is None:
        return MISSING_API_KEY_MESSAGE

    player_context = format_player_context(player_row)

    prompt = f"""
You are acting as a data analyst for an NBA front office.

Write a concise scouting-style summary using only the statistics provided below.
Do not make up information.
Do not mention injuries, contracts, leadership, personality, or off-court factors.
If a claim is not supported by the data, do not include it.

Structure the response with these sections:

1. Overall Summary
2. Main Strengths
3. Possible Concerns
4. Analyst Recommendation

Keep the writing clear and professional, but not overly formal.

Player Data:
{player_context}
"""

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        return response.output_text

    except Exception as e:
        return f"AI summary could not be generated. Error: {e}"


def generate_top_players_summary(top_df, question_type, selected_season, selected_stat_label):
    client = get_openai_client()

    if client is None:
        return MISSING_API_KEY_MESSAGE

    top_players_context = format_top_players_context(top_df, selected_stat_label)

    prompt = f"""
You are a data analyst explaining NBA player rankings to a general audience.

Use only the data provided below.
Do not make up context.
Do not mention injuries, contracts, awards, or narratives unless they appear in the data.

Question Type: {question_type}
Season: {selected_season}
Selected Stat: {selected_stat_label}

Write a short analyst summary that explains:
1. What the ranking shows
2. Which players stand out
3. Any important limitations of using this stat alone

Data:
{top_players_context}
"""

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        return response.output_text

    except Exception as e:
        return f"AI summary could not be generated. Error: {e}"


def generate_player_comparison_summary(player1_row, player2_row, selected_stats):
    client = get_openai_client()

    if client is None:
        return MISSING_API_KEY_MESSAGE

    player1_context = format_player_context(player1_row)
    player2_context = format_player_context(player2_row)

    selected_stat_text = ", ".join(selected_stats)

    prompt = f"""
You are a data analyst comparing two NBA players.

Use only the provided statistics.
Do not make up information.
Do not mention injuries, contracts, leadership, awards, or off-court factors.
Compare the players based on the selected stats: {selected_stat_text}.

Structure the response with:
1. Overall Comparison
2. Where Player 1 Stands Out
3. Where Player 2 Stands Out
4. Final Takeaway

Player 1 Data:
{player1_context}

Player 2 Data:
{player2_context}
"""

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        return response.output_text

    except Exception as e:
        return f"AI comparison could not be generated. Error: {e}"
