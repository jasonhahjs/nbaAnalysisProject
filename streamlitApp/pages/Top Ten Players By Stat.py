import streamlit as st
from streamlitApp.loadData import nba_data, statLabels, reverseLabels

df = nba_data()

st.title("Top 10 Players By Stat")

# Description and instructions
st.markdown("""
### Function Description

This tool allows you to view the top 10 NBA players based on any selected performance statistic, 
such as Points Per Game or True Shooting %. You can filter results by one or multiple seasons.
""")

# Stat selection
selected_label = st.selectbox("Select a Stat", list(statLabels.values()))
selected_stat = reverseLabels[selected_label]

# Season multiselect
available_seasons = sorted(df["season_display"].dropna().unique(), reverse=True)
selected_seasons = st.multiselect("Select Season(s)", available_seasons, default=[available_seasons[0]])

# Ensure stat and season(s) are selected
if not selected_stat or not selected_seasons:
    st.warning("Please select both a stat and at least one season.")
else:
    # Filter for selected seasons
    filtered_df = df[df["season_display"].isin(selected_seasons)]

    if filtered_df.empty:
        st.error("No data available for the selected season(s).")
    else:
        # Sort and show top 10 players
        top_df = filtered_df.sort_values(by=selected_stat, ascending=False).head(10)

        # Stat display checkboxes
        st.subheader("Select Stats to Display in Table")
        default_display = ["PTS_PER_GAME", "REB_PER_GAME", "AST_PER_GAME"]
        selected_display_stats = [
            stat for stat in statLabels.keys()
            if st.checkbox(statLabels[stat], value=stat in default_display)
        ]

        columns_to_display = ["PLAYER_NAME", "TEAM_ABBREVIATION", "season_display", "GP"] + selected_display_stats
        st.dataframe(top_df[columns_to_display])
