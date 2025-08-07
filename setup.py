import os
import subprocess
import sys
import importlib.util

#methods
def run_cmd(cmd, shell=False):
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True, shell=shell)

def is_installed(pkg):
    return importlib.util.find_spec(pkg) is not None

def install_missing(packages):
    missing = [pkg for pkg in packages if not is_installed(pkg)]
    if missing:
        print(f"installing: {missing}")
        run_cmd([venv_python, "-m", "pip", "install", *missing])
    else:
        print("required packages are already installed.")

# Step 1: Create venv if not exists
if not os.path.exists("venv"):
    print("creating venv")
    run_cmd([sys.executable, "-m", "venv", "venv"])
else:
    print("venv already exists.")

# Step 2: Define platform-specific Python path from venv
venv_python = os.path.join("venv", "Scripts", "python.exe") if os.name == "nt" else os.path.join("venv", "bin", "python")

# Step 3: Install required packages
required_packages = ["streamlit", "pandas", "plotly", "nba_api", "seaborn", "matplotlib"]
install_missing(required_packages)

# Step 4: Run any setup scripts
print("running downloadData.py")
run_cmd([venv_python, os.path.join("data", "downloadData.py")])

# Step 5: Launch the app
print("launching Streamlit app")
run_cmd([venv_python, "-m", "streamlit", "run", os.path.join("streamlitApp", "About.py")])
