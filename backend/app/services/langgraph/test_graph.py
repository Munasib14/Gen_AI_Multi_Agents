from typing import TypedDict
from langgraph.graph import StateGraph
import re
from typing import Dict
# imports from sibling 'agent' folder
from backend.app.services.agent.test_agent.testagent_files.metadata_logger  import log_metadata
from backend.app.services.agent.test_agent.testagent_files.metadata_logger  import log_metadata
from backend.app.services.agent.test_agent.testagent_files.validator import validate_conversion_input
from backend.app.services.agent.common_files.transformer import transform_test
 


# Define shared LangGraph state
class TestState(TypedDict):
    input: str
    output: str

TestState = dict[str, str]

def is_probably_valid_input(code: str) -> bool:
    react_indicators = [
        r'import\s+React', r'from\s+["\']react["\']', r'return\s+\(', r'<\w+', r'function\s+\w+\s*\(', r'const\s+\w+\s*=\s*\(',
    ]
    api_indicators = [
        r'fetch\(', r'axios\.', r'app\.(get|post|put|delete)\(', r'res\.json\(', r'request\s*\(', r'router\.(get|post|put|delete)\(',
    ]
    user_story_indicators = [
        r'As a ', r'I want to ', r'So that ', r'User can', r'Admin should be able to',
    ]
    selenium_indicators = [
        r'driver\.', r'webdriver\.', r'By\.', r'find_element', r'get\(', r'click\(\)', r'send_keys\(',
    ]
    all_indicators = react_indicators + api_indicators + user_story_indicators + selenium_indicators
    return any(re.search(p, code, re.IGNORECASE) for p in all_indicators)

def validate_input(state: TestState) -> TestState:
    input_text = state["input"]
    print(f"Input to validate: {input_text}")  # Log input before validation
    if not is_probably_valid_input(input_text):
        state["output"] = "⚠️ Input does not appear to be valid React code, API handler, user story, or Selenium test. Please check your submission."
        print(f"Validation failed: {state['output']}")  # Log the error message
        return state
    print("Validation passed.")
    return state

def test_agent_main(input_code: str, prompt_name: str = "convert_to_playwright_bdd.j2") -> TestState:
    """
    Executes the Web Agent LangGraph to convert React/API/UserStory/Selenium input into BDD-compatible output.

    Args:
        input_code (str): Source input from React, API handler, user story, or Selenium test.
        prompt_name (str): Name of the prompt template used for the transformation.

    Returns:
        WebState: Dictionary containing both input and transformed output.
    """

    def transform_testagent_with_prompt(state: TestState) -> TestState:
        return transform_test(state, prompt_template=prompt_name)

    print(TestState)
    # Create LangGraph and add nodes
    builder = StateGraph(TestState)

    builder.add_node("check_react_api_compatibility", validate_conversion_input)    
    builder.add_node("log_metadata", log_metadata)
    builder.add_node("transform_test", transform_testagent_with_prompt)

    # Define execution flowc
    builder.set_entry_point("check_react_api_compatibility")
    builder.add_edge("check_react_api_compatibility", "log_metadata")
    builder.add_edge("log_metadata", "transform_test")

    # Compile graph and run the pipeline
    graph = builder.compile()
    return graph.invoke({"input": input_code, "output": ""})
 