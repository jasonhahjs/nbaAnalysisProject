# NBA Efficiency Streamlit App

## Description of Project
This Streamlit application fetches and processes NBA player statistics to provide an interactive analytics and visualization platform. Users can view top performers, compare players, and explore stat-driven insights across multiple seasons. Features include:

- Downloading NBA stats via the NBA API and storing them in a SQLite database  
- Filtering and viewing stats with custom Streamlit visualizations  
- Comparing players side by side  
- Viewing top 10 players by selected statistic  
- Handling schema changes, filtering non-NBA players, and cleaning data

---

## Developer Manual

### Prerequisites
- Python 3.8+  
- `venv` or equivalent virtual environment tool  
- Git for version control  
- Optional: Streamlit account for deployment

### Required Packages
Install dependencies via pip:

```bash
pip install -r requirements.txt
```

Your `requirements.txt` should include:
```
streamlit
pandas
nba_api
plotly
sqlite3  # Note: sqlite3 is in Python’s standard library
```

---

### How to Run or Make Changes

1. **Clone the repository and navigate to the project folder:**

    ```bash
    git clone https://github.com/jasonhahjs/nbaAnalysisProject.git
    cd nbaAnalysisProject
    ```

2. **Set up virtual environment and install dependencies:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # or `venv\Scripts\activate` on Windows
    pip install -r requirements.txt
    ```

3. **Initialize the data:**
    ```bash
    python setup.py
    ```
   This will create a virtual environment, install dependencies, download NBA data, and build your database.

4. **Run the app via Streamlit:**
    ```bash
    streamlit run streamlitApp/About.py
    ```
   Navigate to the provided local URL to explore the app.

---

## Project Structure
```
nbaAnalysisProject/
├── data/
│   └── downloadData.py       # Downloads NBA stats and handles schema
├── streamlitApp/
│   ├── loadData.py           # Data loading and stat calculations
│   ├── About.py              # App entry page
│   ├── Custom Visualization.py
│   ├── Player Side‑By‑Side.py
│   └── Top Ten Players By Stat.py
├── requirements.txt
├── setup.py                  # Automates setup and data download
└── .gitignore                # Lists files/folders to exclude from Git
```
Use Streamlit's sidebar to navigate between "About," "Visual Comparison," "Side-by-Side Comparison," and "Top Ten by Stat."

---

## Deployment (Optional)
Deploy the app using [Streamlit Community Cloud](https://streamlit.io/cloud):
- Push your code to GitHub.  
- Connect the repo on Streamlit Cloud.  
- The app will automatically deploy and update with new commits.

---

## Feedback and Contributions
Suggestions and contributions are welcome! To contribute:
1. Fork the repository  
2. Create a feature branch (e.g., `feature/visual-charts`)  
3. Commit changes and open a pull request

---

## About
Built by Jason H. for NBA statistical exploration and insights. Enjoy comparing player efficiency and performance across seasons.
