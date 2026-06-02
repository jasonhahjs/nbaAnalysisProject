import streamlit as st
import pandas as pd

from streamlitApp.loadData import nba_data
from streamlitApp.aiInsights import generate_player_summary


df = nba_data()


st.title("AI Scouting Report Generator")


st.markdown("""
This page uses NBA player statistics to generate an AI-assisted scouting report. 
The purpose is to show how AI can help a data analyst communicate insights clearly while still grounding the response in real data.

The report is based only on the displayed statistics.
""")


available_seasons = sorted(df["season_display"].dropna().unique(), reverse=True)


selected_season = st.selectbox(
    "Select Season",
    available_seasons
)


season_df = df[df["season_display"] == selected_season]


selected_player = st.selectbox(
    "Select Player",
    sorted(season_df["PLAYER_NAME"].dropna().unique())
)


player_row = season_df[season_df["PLAYER_NAME"] == selected_player].iloc[0]


st.markdown("---")


col1, col2 = st.columns([1, 3])


with col1:
    st.image(
        f"https://cdn.nba.com/headshots/nba/latest/260x190/{player_row['PLAYER_ID']}.png",
        width=150
    )


with col2:
    st.subheader(f"{selected_player} - {selected_season}")
    st.write(f"Team: {player_row['TEAM_ABBREVIATION']}")
    st.write(f"Games Played: {player_row['GP']}")
    st.write(f"Scoring Profile: {player_row['SCORING_PROFILE']}")
    st.write(f"Availability Profile: {player_row['AVAILABILITY_PROFILE']}")


st.markdown("### Supporting Data")


supporting_data = pd.DataFrame({
    "Metric": [
        "Points Per Game",
        "Rebounds Per Game",
        "Assists Per Game",
        "Turnovers Per Game",
        "Minutes Per Game",
        "Steals Per Game",
        "Blocks Per Game",
        "True Shooting %",
        "Field Goal %",
        "Win %",
        "Plus-Minus",
        "Basic Impact Score",
        "Scoring Profile",
        "Availability Profile"
    ],
    "Value": [
        player_row.get("PTS_PER_GAME"),
        player_row.get("REB_PER_GAME"),
        player_row.get("AST_PER_GAME"),
        player_row.get("TOV_PER_GAME"),
        player_row.get("MIN_PER_GAME"),
        player_row.get("STL_PER_GAME"),
        player_row.get("BLK_PER_GAME"),
        player_row.get("TS_PCT"),
        player_row.get("FG_PCT"),
        player_row.get("W_PCT"),
        player_row.get("PLUS_MINUS"),
        player_row.get("BASIC_IMPACT_SCORE"),
        player_row.get("SCORING_PROFILE"),
        player_row.get("AVAILABILITY_PROFILE")
    ]
})


st.dataframe(supporting_data, use_container_width=True)


st.markdown("---")


if st.button("Generate AI Scouting Report"):
    with st.spinner("Generating report..."):
        summary = generate_player_summary(player_row)

    st.markdown("### AI-Generated Scouting Report")
    st.write(summary)

    st.info(
        "This report is generated from the displayed statistics only. "
        "It should be treated as an AI-assisted interpretation, not a complete scouting evaluation."
    )