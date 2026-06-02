import streamlit as st
import pandas as pd

from streamlitApp.loadData import nba_data, statLabels
from streamlitApp.aiInsights import generate_player_comparison_summary


df = nba_data()


st.title("Side-by-Side Player Comparison")


st.markdown("""
### Function Description

This tool allows you to compare two NBA players' performance statistics side by side for any selected season. 
You can use it to analyze player efficiency, production, and impact across different timeframes.

The optional AI comparison turns the selected statistics into a short analyst-style explanation.
""")


available_seasons = sorted(df["season_display"].dropna().unique(), reverse=True)


col1, col2 = st.columns(2)


with col1:
    st.markdown("### Player 1")
    season1 = st.selectbox("Select Season", available_seasons, key="season1")
    season1_df = df[df["season_display"] == season1]
    player1 = st.selectbox(
        "Select Player",
        sorted(season1_df["PLAYER_NAME"].dropna().unique()),
        key="player1"
    )


with col2:
    st.markdown("### Player 2")
    season2 = st.selectbox("Select Season", available_seasons, key="season2")
    season2_df = df[df["season_display"] == season2]
    player2 = st.selectbox(
        "Select Player",
        sorted(season2_df["PLAYER_NAME"].dropna().unique()),
        key="player2"
    )


st.markdown("### Stats to Compare")


default_stats = [
    "PTS_PER_GAME",
    "REB_PER_GAME",
    "AST_PER_GAME",
    "TS_PCT",
    "W_PCT",
    "BASIC_IMPACT_SCORE"
]


selected_stats = [
    stat for stat in statLabels.keys()
    if st.checkbox(statLabels[stat], value=stat in default_stats)
]


if player1 == player2 and season1 == season2:
    st.info("Please select two different players or seasons.")
elif not selected_stats:
    st.warning("Please select at least one stat to compare.")
else:
    data1 = season1_df[season1_df["PLAYER_NAME"] == player1].iloc[0]
    data2 = season2_df[season2_df["PLAYER_NAME"] == player2].iloc[0]

    st.markdown("---")
    st.markdown("### Player Info")

    col1, col2 = st.columns(2)

    with col1:
        st.image(
            f"https://cdn.nba.com/headshots/nba/latest/260x190/{data1['PLAYER_ID']}.png",
            width=150
        )
        st.markdown(f"**{player1}** ({season1})")
        st.markdown(f"Team: `{data1['TEAM_ABBREVIATION']}`")
        st.markdown(f"GP: `{data1['GP']}`")
        st.markdown(f"Scoring Profile: `{data1['SCORING_PROFILE']}`")
        st.markdown(f"Availability: `{data1['AVAILABILITY_PROFILE']}`")

    with col2:
        st.image(
            f"https://cdn.nba.com/headshots/nba/latest/260x190/{data2['PLAYER_ID']}.png",
            width=150
        )
        st.markdown(f"**{player2}** ({season2})")
        st.markdown(f"Team: `{data2['TEAM_ABBREVIATION']}`")
        st.markdown(f"GP: `{data2['GP']}`")
        st.markdown(f"Scoring Profile: `{data2['SCORING_PROFILE']}`")
        st.markdown(f"Availability: `{data2['AVAILABILITY_PROFILE']}`")

    st.markdown("---")
    st.markdown("### Stat Comparison")

    comp_df = pd.concat(
        [
            data1[selected_stats].to_frame(name=f"{player1} ({season1})"),
            data2[selected_stats].to_frame(name=f"{player2} ({season2})")
        ],
        axis=1
    )

    comp_df.index = [statLabels.get(stat, stat) for stat in comp_df.index]

    st.dataframe(comp_df, use_container_width=True)

    st.markdown("---")

    if st.button("Generate AI Player Comparison"):
        with st.spinner("Generating AI comparison..."):
            summary = generate_player_comparison_summary(
                player1_row=data1,
                player2_row=data2,
                selected_stats=[statLabels.get(stat, stat) for stat in selected_stats]
            )

        st.subheader("AI-Generated Player Comparison")
        st.write(summary)

        st.info(
            "This AI comparison is based only on the selected statistics shown in the table."
        )