import re

def get_variable_values(variable_list):
    """Prompt the user to enter values for required variables, using defaults if available."""
    variables = {}

    for var in variable_list:
        if isinstance(var, dict):  # If it's a dictionary, extract the key-value pair
            key = list(var.keys())[0]
            default_value = var[key]  # Extract default value if provided
        elif isinstance(var, str):  # If it's a string (e.g., "var=value"), extract before "="
            parts = var.split("=")
            key = parts[0].strip()
            default_value = parts[1].strip() if len(parts) > 1 else ""
        else:
            print(f"Skipping invalid variable format: {var}")
            continue

        user_input = input(f"Enter value for '{key}' (default: {default_value}): ").strip()
        variables[key] = user_input if user_input else default_value  # Use input if provided, otherwise default

    return variables

def replace_variables(text, variables):
    """Replace placeholders in the prompt text with user-provided variable values."""
    if not text:
        return ""

    if isinstance(text, list):  # If the text is a list, join it into a single string
        text = "\n".join(text)

    def replace_match(match):
        var_name = match.group(1)
        return variables.get(var_name, f"[{var_name}]")  # Keep original if not found
    
    return re.sub(r"\[([a-zA-Z0-9_-]+)\]", replace_match, text)
