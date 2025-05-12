# web_prompt_engine.py

import os
from jinja2 import Environment, FileSystemLoader

# Define the path to the web prompts directory
WEB_PROMPT_DIR = os.path.join(os.path.dirname(__file__), "web_prompts")  # Adjust path to web_prompts folder

# Create an environment with the correct loader for the web prompts
env = Environment(loader=FileSystemLoader(WEB_PROMPT_DIR))

def load_web_prompt(template_name: str, context: dict) -> str:
    """
    Loads and renders a Jinja2 template for the Web Agent.

    Args:
        template_name (str): The name of the prompt template file (including .j2).
        context (dict): The context to render the template with.

    Returns:
        str: The rendered prompt template or an error message if something goes wrong.
    """
    try:
        # Load the template from the web prompts directory
        template = env.get_template(template_name)

        # Render and return the template with the given context
        return template.render(context)
    except Exception as e:
        # In case of any error, print and return the error message
        print(f"Error loading template {template_name}: {str(e)}")
        return f"Error loading template: {str(e)}"
