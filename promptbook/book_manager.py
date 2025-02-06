import os
import yaml
import getpass  # Get OS username

def create_prompt_book():
    """Interactively create a new prompt book."""
    print("\n📖 Create a New Prompt Book\n")

    # Detect OS username and use as default author
    author = getpass.getuser()
    author = input(f"Enter Author Name (default: {author}): ").strip() or author

    book_name = input("Enter Book Name: ").strip().replace(" ", "-").lower()
    description = input("Enter Book Description: ").strip()

    # Define book structure
    book_path = os.path.join(os.getcwd(), book_name)
    prompts_path = os.path.join(book_path, "prompts")
    os.makedirs(prompts_path, exist_ok=True)

    # Create prompt-book.yaml
    book_metadata = {
        "author": author,
        "name": book_name,
        "description": description
    }
    with open(os.path.join(book_path, "prompt-book.yaml"), "w", encoding="utf-8") as f:
        yaml.dump(book_metadata, f, default_flow_style=False)

    # Create an example .prompt file inside /prompts
    example_prompt = {
        "author": author,
        "name": "test-prompt",
        "description": "This is a sample prompt.",
        "variables": [{"name": "User"}],
        "prompt": ["Hello [name], welcome to your prompt book!"]
    }
    with open(os.path.join(prompts_path, "test-prompt.prompt"), "w", encoding="utf-8") as f:
        yaml.dump(example_prompt, f, default_flow_style=False)

    print(f"\n✅ Successfully created new book at: {book_path}")
    print(f"📂 Structure:\n  {book_path}/\n    prompt-book.yaml\n    /prompts/\n      test-prompt.prompt\n")

