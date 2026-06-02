# NBA Player Analysis Dashboard

An interactive Streamlit dashboard for exploring NBA player performance across seasons. The app uses locally stored NBA statistics, derived performance metrics, interactive visualizations, and optional OpenAI-powered summaries to help users compare players and explain trends in the data.

## Features

- **Top 10 Players By Stat**: Rank players by scoring, rebounding, assists, efficiency, impact score, and other metrics across one or more seasons.
- **Custom Visualization**: Build interactive scatter plots that compare any two selected statistics.
- **Player Side-By-Side**: Compare two players across selected seasons and metrics, with optional AI-generated comparison notes.
- **AI Scouting Report Generator**: Generate a scouting-style summary for a selected player using only the displayed statistical data.

## Project Structure

```text
NBA Dashboard Project/
|-- data/
|   |-- downloadData.py       # Downloads NBA data and builds the SQLite database
|   `-- nba_stats.db          # Local SQLite database
|-- streamlitApp/
|   |-- About.py              # Main Streamlit entrypoint
|   |-- aiInsights.py         # OpenAI-powered summary helpers
|   |-- loadData.py           # Loads and prepares player data
|   `-- pages/
|       |-- AI Scouting Report Generator.py
|       |-- Custom Visualization.py
|       |-- Player Side-By-Side.py
|       `-- Top Ten Players By Stat.py
|-- .env.example              # Example environment variable file
|-- .gitignore
|-- README.md
`-- setup.py                  # Creates venv, installs packages, downloads data, launches app
```

## Tech Stack

- Python
- Streamlit
- Pandas
- Plotly
- SQLite
- nba_api
- OpenAI API
- python-dotenv

## Setup

### 1. Clone the Repository

```bash
git clone git@github.com:jasonhahjs/nbaAnalysisProject.git
cd nbaAnalysisProject
```

### 2. Run the Setup Script

```bash
python setup.py
```

The setup script will:

- Create a virtual environment if one does not already exist.
- Install the required Python packages.
- Download NBA player data into the local SQLite database.
- Launch the Streamlit app.

The first run can take several minutes because the app needs to download and store NBA data.

## Running the App Manually

If dependencies and data are already set up, run:

```bash
streamlit run streamlitApp/About.py
```

On Windows, if you are using the included virtual environment:

```powershell
.\venv\Scripts\streamlit.exe run streamlitApp\About.py
```

## OpenAI API Setup

The dashboard works without an OpenAI API key for normal data exploration. AI features require an API key.

1. Create an API key at [platform.openai.com/api-keys](https://platform.openai.com/api-keys).
2. Copy `.env.example` to `.env`.
3. Replace the placeholder value with your real key:

```text
OPENAI_API_KEY=your_real_api_key_here
```

The `.env` file should be placed in the project root, next to `setup.py`.

Do not commit `.env` to GitHub. It is listed in `.gitignore` so your key stays private.

OpenAI API usage may cost money. The app uses API calls only when you click an AI summary or scouting report button.

## Data Source

Player data is pulled with `nba_api`, stored locally in SQLite, and loaded into the Streamlit dashboard with Pandas.

The app also calculates derived metrics such as:

- Points, rebounds, assists, steals, blocks, turnovers, and minutes per game
- True shooting percentage
- Basic impact score
- Scoring efficiency profile
- Availability profile

## Current Pages

- `About.py`
- `Top Ten Players By Stat.py`
- `Custom Visualization.py`
- `Player Side-By-Side.py`
- `AI Scouting Report Generator.py`

The former Data Assistant page has been removed from the project.

## Troubleshooting

### `OPENAI_API_KEY is not set`

Make sure your `.env` file is in the project root and contains:

```text
OPENAI_API_KEY=your_real_api_key_here
```

Restart Streamlit after editing `.env`.

### `401 invalid_api_key`

The app found an API key, but the key is invalid or still set to the placeholder. Create a new key from the OpenAI dashboard and update `.env`.

### Streamlit Still Shows an Old Page

Stop and restart the Streamlit server:

```powershell
Ctrl + C
.\venv\Scripts\streamlit.exe run streamlitApp\About.py
```

## Future Improvements

- Add player career averages.
- Add playoff statistics.
- Add team-level analysis.
- Add more advanced impact metrics.
- Add saved chart exports.

## Developer

Created by **Jason Ha**

- GitHub: [@jasonhahjs](https://github.com/jasonhahjs)
- LinkedIn: [@jasonhahjs](https://www.linkedin.com/in/jasonhahjs/)
