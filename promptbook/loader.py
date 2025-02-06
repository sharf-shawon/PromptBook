import os
import yaml  # Ensure this is present!

PROMPT_FOLDERS = ["library", "prompts"]

def find_prompt(prompt_name):
    """Search for a prompt file in the defined folders, including cloned prompt books."""
    for folder in PROMPT_FOLDERS:
        for root, _, files in os.walk(folder):
            file_path = os.path.join(root, f"{prompt_name}.prompt")
            if os.path.exists(file_path):
                return file_path
    return None

def load_prompt(file_path):
    """Load and parse the YAML prompt file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)  # Ensure this line has access to `yaml`
    except Exception as e:
        print(f"Error loading prompt file: {e}")
        return None
