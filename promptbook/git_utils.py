import os
import shutil
import subprocess
import yaml
from pathlib import Path
from urllib.parse import urlparse

LIBRARY_PATH = "library"
TEMP_DIR = "temp_repo"

def extract_github_username(repo_url):
    """Extract GitHub username from a given repository URL."""
    parsed_url = urlparse(repo_url)
    path_parts = parsed_url.path.strip("/").split("/")
    return path_parts[0] if len(path_parts) > 1 else "unknown_user"

def clone_prompt_book(repo_url):
    """Clone a Git repository, validate the prompt book, and store it in the library."""
    
    # Extract GitHub username from URL
    github_username = extract_github_username(repo_url)
    
    print(f"Cloning repository: {repo_url}")
    
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    
    try:
        subprocess.run(["git", "clone", "--depth", "1", repo_url, TEMP_DIR], check=True)
    except subprocess.CalledProcessError:
        print("❌ Failed to clone repository.")
        return False

    prompt_book_path = Path(TEMP_DIR) / "prompt-book.yaml"
    if not prompt_book_path.exists():
        print("❌ No 'prompt-book.yaml' found. Not a valid prompt book repository.")
        shutil.rmtree(TEMP_DIR)
        return False

    try:
        with open(prompt_book_path, "r", encoding="utf-8") as file:
            book_data = yaml.safe_load(file)
    except Exception as e:
        print(f"❌ Error reading 'prompt-book.yaml': {e}")
        shutil.rmtree(TEMP_DIR)
        return False

    book_name = book_data.get("name", "").strip()

    if not github_username or not book_name:
        print("❌ Invalid metadata in 'prompt-book.yaml'. Missing author or name.")
        shutil.rmtree(TEMP_DIR)
        return False

    # Store the book under `library/{GitHub Username}/{Book Name}`
    target_dir = Path(LIBRARY_PATH) / github_username / book_name
    if target_dir.exists():
        print(f"⚠️ Book '{book_name}' by '{github_username}' already exists. Overwriting...")
        shutil.rmtree(target_dir)

    shutil.move(TEMP_DIR, target_dir)
    print(f"✅ Successfully cloned '{book_name}' by '{github_username}' into '{target_dir}'")

    return True
