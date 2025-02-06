import json
import yaml
import requests
import uuid
import os
from promptbook.loader import find_prompt, load_prompt
from promptbook.utils import get_variable_values, replace_variables

from promptbook.config_manager import load_config

config = load_config()


def check_model_exists(model, tags_url):
    """Check if the specified model exists in Ollama."""
    try:
        response = requests.get(tags_url)
        response.raise_for_status()
        models = response.json().get("models", [])
        available_models = [m["name"] for m in models]

        if model in available_models:
            return True
        else:
            print(f"⚠️ Model '{model}' not found in Ollama. Available models: {available_models}")
            return False
    except requests.RequestException as e:
        print(f"⚠️ Could not retrieve model list from Ollama: {e}")
        return False


def send_to_ollama(messages, session_id):
    """Send a conversation to Ollama and maintain session context."""
    config = load_config()
    model = config.get("ollama", {}).get("model", "llama3:2b")
    stream = config.get("ollama", {}).get("stream", True)
    debug = config.get("ollama", {}).get("debug", False)
    api_url = config.get("ollama", {}).get("api_url", "http://localhost:11434/api/chat")
    tags_url = config.get("ollama", {}).get("tags_url", "http://localhost:11434/api/tags")

    if not check_model_exists(model, tags_url):
        return f"⚠️ Model '{model}' is not available in Ollama.", session_id

    payload = {
        "model": model,
        "messages": messages,
        "context": session_id,
        "stream": stream
    }

    try:
        response = requests.post(api_url, json=payload, headers={"Content-Type": "application/json"}, stream=stream)
        response.raise_for_status()

        if debug:
            print(f"🔍 Debug: Raw API Response: {response.text}")

        full_response = []
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line)
                    if "message" in data and "content" in data["message"]:
                        full_response.append(data["message"]["content"])
                    if data.get("done", False):
                        break
                except json.JSONDecodeError as e:
                    print(f"⚠️ Streaming JSON Decode Error: {e}. Raw line: {line}")

        return "".join(full_response), session_id
    except requests.RequestException as e:
        print(f"⚠️ Ollama request failed: {e}")
        return retry_request(payload, session_id, api_url)


def retry_request(payload, session_id, api_url, retries=3):
    """Retry Ollama request in case of failure."""
    for attempt in range(retries):
        try:
            response = requests.post(api_url, json=payload, headers={"Content-Type": "application/json"}, stream=True)
            response.raise_for_status()
            return response.text, session_id
        except requests.RequestException as e:
            print(f"⚠️ Retry {attempt + 1}/{retries} failed: {e}")
    return "⚠️ Ollama request failed after retries.", session_id


def process_single_prompt(prompt_data, prompt_name):
    """Process a single prompt file, including fetching missing variables."""
    prompt_file = find_prompt(prompt_name)
    if not prompt_file:
        print(f"⚠️ Warning: Prompt '{prompt_name}' not found. Skipping.")
        return ""

    prompt_data = load_prompt(prompt_file)
    if not prompt_data:
        print(f"⚠️ Warning: Failed to load '{prompt_name}'. Skipping.")
        return ""

    prompt_text = prompt_data.get("prompt", "")
    if isinstance(prompt_text, list):
        prompt_text = "\n".join(prompt_text)

    print(f"\n📜 Prompt: {prompt_text}\n")
    variables = get_variable_values(prompt_data.get("variables", []))
    return replace_variables(prompt_text, variables)


def process_prompt(prompt_data):
    """Process the prompt and its pre/post-prompts while keeping variable scopes separate."""
    output_chain = []
    session_id = str(uuid.uuid4())  # Unique ID for maintaining Ollama session
    messages = []  # Maintain conversation history

    def process_prompt_items(prompt_text, variables):
        """Process and output prompt items according to config settings."""
        separator = config.get("separator", "~")
        ollama_enabled = config.get("ollama", {}).get("enabled", False)

        if isinstance(prompt_text, list):
            prompt_text = "\n".join(prompt_text)

        processed_text = replace_variables(prompt_text, variables)
        output_lines = processed_text.split("\n")

        if not ollama_enabled:
            # Output all prompt items with separator
            formatted_output = f" {separator} ".join(line.strip() for line in output_lines if line.strip())
            print(f"\n📜 Prompt Output:\n{formatted_output}\n")
            return

        # Otherwise, send to Ollama
        messages = []
        session_id = str(uuid.uuid4())
        
        for line in output_lines:
            if line.strip():
                print(f"\n💬 Sending: {line}")
                messages.append({"role": "user", "content": line})
                response, session_id = send_to_ollama(messages, session_id)
                print(f"🧠 Ollama Response: {response}")
                messages.append({"role": "assistant", "content": response})


    for pre_prompt in prompt_data.get("pre-prompt", []):
        pre_prompt_name = pre_prompt.get("prompt")
        print(f"\n🟢 Processing Pre-Prompt: {pre_prompt_name}\n")
        pre_prompt_output = process_single_prompt(pre_prompt, pre_prompt_name)
        process_prompt_items(pre_prompt_output, {})

    print("\n🔵 Processing Main Prompt...\n")
    process_prompt_items(prompt_data.get("prompt", ""), get_variable_values(prompt_data.get("variables", [])))

    for post_prompt in prompt_data.get("post-prompt", []):
        post_prompt_name = post_prompt.get("prompt")
        print(f"\n🟠 Processing Post-Prompt: {post_prompt_name}\n")
        post_prompt_output = process_single_prompt(post_prompt, post_prompt_name)
        process_prompt_items(post_prompt_output, {})

    print("\n✅ Execution Complete.")
