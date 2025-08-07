# NBA Player Analysis Project

## Overview
The **NBA Player Analysis App** is an interactive Streamlit application for exploring NBA player performance data using advanced stats, visual comparisons, and rankings. Built using Python, SQLite, and `nba_api`, the app is ideal for fans, students, and analysts looking to explore player efficiency and trends from 1996 onward.

> “Instead of relying on hot takes, use real data to shape your NBA opinions.”

---

## Project Structure

```bash
nbaAnalysisProject/
├── data/
│   ├── nba_stats.db             # SQLite database storing NBA player stats
│   └── downloadData.py          # Script to download and populate stats via nba_api
├── streamlitApp/
│   ├── About.py                 # Main dashboard landing page
│   ├── Custom Visualization.py  # Visual stat comparison (scatter plot)
│   ├── Player Side-By-Side.py   # Compare two players head-to-head
│   ├── Top Ten Players By Stat.py # Ranks top players by selected stat
│   └── loadData.py              # Loads and prepares data from database
├── setup.py                     # Setup script (installs deps, runs download, launches app)
├── requirements.txt             # Python dependency list (optional if using setup.py)
└── README.md                    # You're reading it!
```

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/jasonhahjs/nbaAnalysisProject
cd nbaAnalysisProject
```

### 2. Run the Setup Script
```bash
python setup.py
```

This will:
- Create a virtual environment (if missing)
- Install required packages: `streamlit`, `pandas`, `nba_api`, `plotly`, etc.
- Download and store NBA stats in a local database
- Launch the Streamlit app automatically

> First-time setup may take a few minutes while all seasons are downloaded.

---

## App Features

### Top 10 Players By Stat
- Choose a season and stat (e.g., Points Per Game, True Shooting %)
- View the top 10 players with sortable and selectable columns

### Visual Comparison
- Create a scatter plot of any two stats
- Filter by season and limit the number of players shown
- Color-coded by team for readability

### Side-by-Side Player Comparison
- Compare two players across seasons
- Choose which metrics to view (PPG, TS%, AST, etc.)
- View headshots, team, and stat breakdowns

---

## Data Source

- `nba_api`: Data is pulled from the official NBA Stats API
- Filtered for real NBA teams only (excluding G-League, WNBA, etc.)
- Stats exclude players with fewer than 20 games played

---

## Technologies Used

- Streamlit for dashboard
- nba_api for data ingestion
- SQLite for local storage
- Pandas for data processing
- Plotly for interactive visuals

---

## Sample Metrics Available

| Code           | Description               |
|----------------|---------------------------|
| `PTS_PER_GAME` | Points Per Game (PPG)     |
| `REB_PER_GAME` | Rebounds Per Game (RPG)   |
| `AST_PER_GAME` | Assists Per Game (APG)    |
| `TS_PCT`       | True Shooting %           |
| `W_PCT`        | Win %                     |
| `TOV_PER_GAME` | Turnovers Per Game (TOPG) |
| `MIN_PER_GAME` | Minutes Per Game (MPG)    |
| `PLUS_MINUS`   | Plus-Minus                |

More can be selected dynamically in the app!

---

## Future Enhancements

- [ ] Add player career averages
- [ ] Expand to include playoff stats
- [ ] Add team-wide analysis features
- [ ] Export charts and comparisons to PDF or CSV

---

## About the Developer

**Jason Ha**  
GitHub: [@jasonhahjs](https://github.com/jasonhahjs)

Built to combine a love of basketball, programming, and data analytics.  
Feedback, contributions, and ideas are always welcome!

---

## Screenshots

(Add screenshots or GIFs of the interface if you’d like)

---

## License

This project is licensed under the MIT License.

---

## Acknowledgments

- NBA Stats API
- swar/nba_api
- Streamlit community for dashboard inspiration
