import json
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve()

SCRIPT_DIR = SCRIPT_PATH.parent

PROJECT_ROOT = SCRIPT_DIR.parent.parent

CONFIG_DIR = PROJECT_ROOT / "storage" / "data"

CONFIG_FILE = CONFIG_DIR / "settings.json"

DEFAULT_SETTINGS = {
    "theme": "dark"
}


def load_settings():
    if not CONFIG_FILE.exists():
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS

    with open(CONFIG_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print("Configuração corrompida, usando padrões.")
            return DEFAULT_SETTINGS


def save_settings(settings: dict):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(settings, f, indent=4)