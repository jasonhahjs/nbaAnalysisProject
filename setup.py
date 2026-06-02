import os
import subprocess
import sys
import importlib.util


# Absolute path to the folder where setup.py is located
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


def run_cmd(cmd, shell=False):
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True, shell=shell, cwd=PROJECT_ROOT)


def is_installed(pkg):
    return importlib.util.find_spec(pkg) is not None


# Step 1: Create venv if it does not exist
venv_path = os.path.join(PROJECT_ROOT, "venv")

if not os.path.exists(venv_path):
    print("Creating venv")
    run_cmd([sys.executable, "-m", "venv", venv_path])
else:
    print("venv already exists.")


# Step 2: Define platform-specific Python path from venv
if os.name == "nt":
    venv_python = os.path.join(venv_path, "Scripts", "python.exe")
else:
    venv_python = os.path.join(venv_path, "bin", "python")


def install_missing(packages):
    missing = []

    for pkg in packages:
        package_name = pkg.split("==")[0].replace("-", "_")

        if importlib.util.find_spec(package_name) is None:
            missing.append(pkg)

    if missing:
        print(f"Installing: {missing}")
        run_cmd([venv_python, "-m", "pip", "install", *missing])
    else:
        print("Required packages are already installed.")


# Step 3: Install required packages
required_packages = [
    "streamlit",
    "pandas",
    "plotly",
    "nba_api",
    "seaborn",
    "matplotlib",
    "openai",
    "python-dotenv"
]

install_missing(required_packages)


# Step 4: Run downloadData.py
download_script = os.path.join(PROJECT_ROOT, "data", "downloadData.py")

if not os.path.exists(download_script):
    raise FileNotFoundError(f"Could not find downloadData.py at: {download_script}")

print("Running downloadData.py")
run_cmd([venv_python, download_script])


# Step 5: Launch the app
about_page = os.path.join(PROJECT_ROOT, "streamlitApp", "About.py")

if not os.path.exists(about_page):
    raise FileNotFoundError(f"Could not find About.py at: {about_page}")

print("Launching Streamlit app")
run_cmd([venv_python, "-m", "streamlit", "run", about_page])