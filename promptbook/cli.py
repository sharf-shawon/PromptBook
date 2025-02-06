import argparse
from promptbook.processor import process_prompt
from promptbook.loader import find_prompt, load_prompt
from promptbook.book_manager import create_prompt_book  # Import new function

def main():
    parser = argparse.ArgumentParser(prog="promptbook", description="A prompt library CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Run Prompt
    run_parser = subparsers.add_parser("run", help="Run a prompt")
    run_parser.add_argument("prompt_name", help="Name of the prompt to run")

    # Clone Prompt Book
    clone_parser = subparsers.add_parser("clone", help="Clone a prompt book from a repository")
    clone_parser.add_argument("repo_url", help="Git repository URL of the prompt book")

    # Create New Prompt Book
    create_book_parser = subparsers.add_parser("create-book", help="Create a new prompt book")

    args = parser.parse_args()

    if args.command == "run":
        prompt_file = find_prompt(args.prompt_name)
        if not prompt_file:
            print("❌ Prompt not found.")
            return
        prompt_data = load_prompt(prompt_file)
        if prompt_data:
            process_prompt(prompt_data)
    elif args.command == "clone":
        from promptbook.git_utils import clone_prompt_book
        clone_prompt_book(args.repo_url)
    elif args.command == "create-book":
        create_prompt_book()  # Call function from book_manager.py
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
