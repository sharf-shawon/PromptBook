# 📚 PromptBook

## 📝 Overview
PromptBook is a powerful and flexible prompt management library designed for AI-driven workflows. It allows users to create, manage, and execute prompts efficiently, including pre-prompts and post-prompts. The library integrates seamlessly with **Ollama**, enabling contextual AI conversations across multiple prompts.

## 🚀 Features
- **Create & Manage Prompt Books**: Organize prompts in structured prompt books.
- **Pre & Post-Prompt Execution**: Automatically process dependent prompts before and after the main prompt.
- **Variable Substitution**: Dynamically replace placeholders with user-defined or default values.
- **Ollama Integration**: Run prompts in AI models while maintaining context across multiple prompts.
- **Git-Based Prompt Cloning**: Clone prompt books from Git repositories for shared collaboration.
- **Customizable Configuration**: Modify API settings, debugging options, and more via `config.yaml`.

## 📥 Installation
```sh
pip install promptbook
```

## 🔧 Configuration
After installation, a `config.yaml` file can be created in the project root to customize settings:

```yaml
ollama:
  model: "llama3:2b"
  stream: true
  debug: false
  api_url: "http://localhost:11434/api/chat"
  tags_url: "http://localhost:11434/api/tags"
```

## 📖 Usage
### 1️⃣ Running a Prompt
To execute a prompt from a prompt book:
```sh
promptbook run test-prompt
```

### 2️⃣ Creating a New Prompt Book
To create a new prompt book:
```sh
promptbook create-book
```
The CLI will guide you through setting up the book structure and an initial prompt file.

### 3️⃣ Cloning a Prompt Book from GitHub
```sh
promptbook clone https://github.com/username/promptbook-repo.git
```

### 4️⃣ Debugging API Calls
Enable debug mode in `config.yaml`:
```yaml
debug: true
```

### 5️⃣ Running a Prompt with Ollama
Each item in a prompt list will be executed sequentially while maintaining conversation context.
```sh
promptbook run my-prompt
```
Example output:
```
💬 Sending: What is the capital of France?
🧠 Ollama Response: The capital of France is Paris.
```

## 📂 File Structure
```
my-promptbook/
├── prompt-book.yaml  # Book metadata
├── prompts/
│   ├── test-prompt.prompt
│   ├── another-prompt.prompt
```

## 🛠 Development & Contribution
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/promptbook.git
   cd promptbook
   ```
2. Install dependencies:
   ```sh
   pip install -e .
   ```
3. Run tests:
   ```sh
   pytest tests/
   ```

## 📜 License
This project is licensed under the **MIT License**.

## ✨ Credits
Developed by [Sharfuddin Shawon](https://shawon.me).

