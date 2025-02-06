import os
import yaml

CONFIG_DIR = os.path.expanduser("~/.promptbook")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.yaml")

DEFAULT_CONFIG = {
    "output_mode": "text",  # Default mode is text output (not Ollama)
    "separator": "~",  # Separator between prompt items
    "ollama": {
        "enabled": False,  # Ollama is disabled by default
        "model": "llama3:2b",
        "stream": True,
        "debug": False,
        "api_url": "http://localhost:11434/api/chat",
        "tags_url": "http://localhost:11434/api/tags"
    }
}

def ensure_config_exists():
    """Ensure that the config file exists in the user's home directory."""
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w", encoding="utf-8") as file:
            yaml.dump(DEFAULT_CONFIG, file)
            print(f"✅ Created default config: {CONFIG_FILE}")

def load_config():
    """Load the config from the user's home directory."""
    ensure_config_exists()
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"⚠️ Warning: Failed to load config.yaml. Using default values. Error: {e}")
        return DEFAULT_CONFIG
