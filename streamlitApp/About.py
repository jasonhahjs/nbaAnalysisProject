import streamlit as st

st.set_page_config(
    page_title="NBA Player Analysis Application",
    layout="wide"
)

st.title("NBA Player Analysis Application")
st.markdown("---")

st.markdown("""
Welcome to the **NBA Player Analysis Application**, a data-driven tool that helps you explore and analyze NBA player performance through advanced metrics and interactive visualizations.

### Different App Functions:
- **Top 10 By Stat**: See the best-performing players based on any stat — points, assists, rebounds, and more.
- **Visual Comparison**: Compare players across two performance metrics in an interactive scatterplot.
- **Side-by-Side View**: Compare two players head-to-head across selected key statistics and seasons.

### Data Source:
- This app uses official **NBA statistics**, sourced and updated via the NBA API and stored locally in SQLite.

### Why This App?
Stemming from a mix of curiosity and the endless debates surrounding NBA players, this app was created to give fans and analysts a way to explore the data for themselves. 
Instead of relying on hot takes or biased commentary, you can now select the stats that matter to you and draw your own conclusions about player performance.

---

### About the Developer
Created by **Jason Ha**  
Feel free to [connect on GitHub](https://github.com/jasonhahjs) or suggest features!

""")
