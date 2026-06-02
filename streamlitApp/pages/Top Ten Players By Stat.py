import streamlit as st
from streamlitApp.loadData import nba_data, statLabels, reverseLabels
from streamlitApp.aiInsights import generate_top_players_summary


df = nba_data()


st.title("Top 10 Players By Stat")


st.markdown("""
### Function Description

This tool allows you to view the top 10 NBA players based on any selected performance statistic, 
such as Points Per Game, True Shooting %, or Basic Impact Score. You can filter results by one or multiple seasons.

The optional AI summary explains what the ranking shows in plain language.
""")


selected_label = st.selectbox("Select a Stat", list(statLabels.values()))
selected_stat = reverseLabels[selected_label]


available_seasons = sorted(df["season_display"].dropna().unique(), reverse=True)

selected_seasons = st.multiselect(
    "Select Season(s)",
    available_seasons,
    default=[available_seasons[0]]
)


if not selected_stat or not selected_seasons:
    st.warning("Please select both a stat and at least one season.")
else:
    filtered_df = df[df["season_display"].isin(selected_seasons)]

    if filtered_df.empty:
        st.error("No data available for the selected season(s).")
    else:
        top_df = filtered_df.sort_values(by=selected_stat, ascending=False).head(10)

        st.subheader("Select Stats to Display in Table")

        default_display = [
            "PTS_PER_GAME",
            "REB_PER_GAME",
            "AST_PER_GAME",
            "TS_PCT",
            "BASIC_IMPACT_SCORE"
        ]

        selected_display_stats = [
            stat for stat in statLabels.keys()
            if st.checkbox(statLabels[stat], value=stat in default_display)
        ]

        columns_to_display = [
            "PLAYER_NAME",
            "TEAM_ABBREVIATION",
            "season_display",
            "GP"
        ] + selected_display_stats

        st.dataframe(top_df[columns_to_display], use_container_width=True)

        st.markdown("---")

        if st.button("Generate AI Summary of This Ranking"):
            with st.spinner("Generating AI summary..."):
                selected_season_text = ", ".join(selected_seasons)

                summary = generate_top_players_summary(
                    top_df=top_df,
                    question_type="Top 10 Players By Selected Stat",
                    selected_season=selected_season_text,
                    selected_stat_label=selected_label
                )

            st.subheader("AI-Generated Ranking Summary")
            st.write(summary)

            st.info(
                "This AI summary is based only on the displayed ranking table. "
                "It should be treated as an analyst-style explanation, not a full player evaluation."
            )