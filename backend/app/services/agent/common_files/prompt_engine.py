# prompt_engine.py

import os
from jinja2 import Environment, FileSystemLoader

# Define paths to the prompts directories

# WEB_PROMPT_DIR = r"D:\Multi-Agent\backend\app\services\agent\web_agent\web_prompts"
WEB_PROMPT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "web_agent", "web_prompts")
)
DB_PROMPT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "db_agent", "db_prompts")
)
TEST_PROMPT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "test_agent", "Playwright_prompts")
)
DEV_PROMPT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "devops_agent", "devops_prompts")
)


# PROMPT_DIR = r"D:\Multi-Agent\backend\app\services\agent\db_agent\web_prompts"  # Adjust path to general prompts folder


# Create environments for both web and general prompts
web_env = Environment(loader=FileSystemLoader(WEB_PROMPT_DIR))
db_env = Environment(loader=FileSystemLoader(DB_PROMPT_DIR))
test_env = Environment(loader=FileSystemLoader(TEST_PROMPT_DIR))
dev_env = Environment(loader=FileSystemLoader(DEV_PROMPT_DIR))



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
        print(f"🧪 Loading from: {WEB_PROMPT_DIR}")
        print(f"🧪 Template name: {template_name}")
        print(f"🧪 Context: {context}")

        # Normalize template name
        template_name = template_name.strip().lower()

        # Check if the template exists
        full_path = os.path.join(WEB_PROMPT_DIR, template_name)
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Template {template_name} not found in {WEB_PROMPT_DIR}")

        # Load and render the template
        template = web_env.get_template(template_name)
        return template.render(context)

    except Exception as e:
        print(f"Error loading web template {template_name}: {str(e)}")
        return f"Error loading template: {str(e)}"

def load_db_prompt(template_name: str, context: dict) -> str:
    """
    Loads and renders a Jinja2 template for the DB Agent.

    Args:
        template_name (str): The name of the prompt template file (including .j2).
        context (dict): The context to render the template with.

    Returns:
        str: The rendered prompt template or an error message if something goes wrong.
    """
    try:
        print(f"🧪 Loading from: {DB_PROMPT_DIR}")
        print(f"🧪 Template name: {template_name}")
        print(f"🧪 Context: {context}")

        # Normalize template name
        template_name = template_name.strip().lower()

        # Check if the template exists
        full_path = os.path.join(DB_PROMPT_DIR, template_name)
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Template {template_name} not found in {DB_PROMPT_DIR}")

        # Load and render the template
        template = db_env.get_template(template_name)
        return template.render(context)

    except Exception as e:
        print(f"Error loading DB template {template_name}: {str(e)}")
        return f"Error loading template: {str(e)}"
    

def load_test_prompt(template_name: str, context: dict) -> str:
    """
    Loads and renders a Jinja2 template for the Test Agent.

    Args:
        template_name (str): The name of the prompt template file (including .j2).
        context (dict): The context to render the template with.

    Returns:
        str: The rendered prompt template or an error message if something goes wrong.
    """
    try:
        print(f"🧪 Loading from: {TEST_PROMPT_DIR}")
        print(f"🧪 Template name: {template_name}")
        print(f"🧪 Context: {context}")

        # Normalize template name
        template_name = template_name.strip().lower()

        # Check if the template exists
        full_path = os.path.join(TEST_PROMPT_DIR, template_name)
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Template {template_name} not found in {TEST_PROMPT_DIR}")

        # Load and render the template
        template = test_env.get_template(template_name)
        return template.render(context)

    except Exception as e:
        print(f"Error loading test template {template_name}: {str(e)}")
        return f"Error loading template: {str(e)}"
    
def load_dev_prompt(template_name: str, context: dict) -> str:
    """
    Loads and renders a Jinja2 template for the DevOps Agent.

    Args:
        template_name (str): The name of the prompt template file (including .j2).
        context (dict): The context to render the template with.

    Returns:
        str: The rendered prompt template or an error message if something goes wrong.
    """
    try:
        print(f"🧪 Loading from: {DEV_PROMPT_DIR}")
        print(f"🧪 Template name: {template_name}")
        print(f"🧪 Context: {context}")

        # Normalize template name
        template_name = template_name.strip().lower()

        # Check if the template exists
        full_path = os.path.join(DEV_PROMPT_DIR, template_name)
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Template {template_name} not found in {DEV_PROMPT_DIR}")

        # Load and render the template
        template = dev_env.get_template(template_name)
        return template.render(context)

    except Exception as e:
        print(f"Error loading DevOps template {template_name}: {str(e)}")
        return f"Error loading template: {str(e)}"

    
    