import streamlit as st
import plotly.express as px
import pandas as pd

from streamlitApp.loadData import nba_data, statLabels, reverseLabels

df = nba_data()

st.title("Visual Comparison")
st.markdown("""
### About The Visual Comparison Tool

This interactive chart allows you to compare NBA player statistics across selected seasons. 
You can choose two stats to plot on the X and Y axes (e.g., Points Per Game vs. Assists Per Game) 
and view a scatter plot of the top players based on your selected Y-axis stat.
""")

# Season filter: allow multiple selection
seasons = st.multiselect(
    "Select season(s) to visualize",
    options=sorted(df["season_display"].dropna().unique(), reverse=True),
    default=sorted(df["season_display"].dropna().unique(), reverse=True)[:1]
)

# Only continue if seasons are selected
if not seasons:
    st.warning("Please select at least one season to view the visualization.")
else:
    # Filter by selected seasons
    filtered_df = df[df["season_display"].isin(seasons)]

    # Axis selectors
    x_label = st.selectbox("X-axis Stat", list(statLabels.values()), index=0)
    y_label = st.selectbox("Y-axis Stat", list(statLabels.values()), index=1)
    x_axis = reverseLabels[x_label]
    y_axis = reverseLabels[y_label]

    # Player count slider
    max_players = st.number_input(
        "Number of players to display",
        min_value=1,
        max_value=len(filtered_df),
        value=min(50, len(filtered_df)),
        step=1
    )

    # Sort and slice
    top_df = filtered_df.sort_values(by=y_axis, ascending=False).head(max_players)

    # Plot
    fig = px.scatter(
        top_df,
        x=x_axis,
        y=y_axis,
        color="TEAM_ABBREVIATION",
        hover_data={
            "PLAYER_NAME": True,
            "TEAM_ABBREVIATION": True,
            "season_display": True,
            x_axis: True,
            y_axis: True
        },
        title=f"{y_label} vs {x_label} (Top {max_players})",
        labels={x_axis: x_label, y_axis: y_label, "season_d": "Season"}
    )

    st.plotly_chart(fig)
