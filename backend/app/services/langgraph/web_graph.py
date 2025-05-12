import re
from typing import TypedDict
from langgraph.graph import StateGraph

# imports from sibling 'agent' folder
from backend.app.services.agent.common_files.transformer import transform_web
from backend.app.services.agent.web_agent.web_files.schema_extractor import extract_html_schema
from backend.app.services.agent.web_agent.web_files.validator import check_html_compatibility
from backend.app.services.agent.web_agent.web_files.optimization_tuner import suggest_css_optimizations
from backend.app.services.agent.web_agent.web_files.refactor_component import refactor_component
from backend.app.services.agent.web_agent.web_files.metadata_logger import log_metadata

# Define shared LangGraph state for web transformation
class WebState(TypedDict):
    input: str
    output: str

# Function to check if the input is likely ASP.NET code
def is_probably_aspnet_code(code: str) -> bool:
    aspnet_indicators = [
        r'<%@\s*Page', r'<asp:', r'runat="server"',
        r'<script[^>]*runat="server"', r'<form[^>]*runat="server"',
        r'protected\s+void', r'Page_Load', r'System\.Web\.UI'
    ]
    return any(re.search(pattern, code, re.IGNORECASE) for pattern in aspnet_indicators)

def validate_input(state: WebState) -> WebState:
    input_text = state["input"]
    print(f"Input to validate: {input_text}")  # Log input before validation
    if not is_probably_aspnet_code(input_text):
        state["output"] = "⚠️ This input doesn't look like ASP.NET code. Please provide valid ASP.NET front-end code."
        print(f"Validation failed: {state['output']}")  # Log the error message
        return state  # Return immediately without proceeding further
    print("Validation passed.")
    return state


# Main Web Agent orchestration function
def web_agent_main(html_code: str, prompt_name: str = "convert_asp_net_to_react.j2") -> WebState:
    """
    Executes the Web Agent LangGraph with dynamic prompt support.

    Args:
        html_code (str): Input HTML or ASP.NET code to analyze and transform into React.
        prompt_name (str): Name of the Jinja2 prompt template to use (default is 'convert_asp_net_to_react.j2').

    Returns:
        WebState: Dictionary with both input and LLM-transformed output React code.
    """

    # Transformer step with dynamic prompt injection
    def transform_web_with_prompt(state: WebState) -> WebState:
        return transform_web(state, prompt_template=prompt_name)

    # Create LangGraph and add nodes
    builder = StateGraph(WebState)

    # Add all nodes including validation
    builder.add_node("validate_input", validate_input)
    builder.add_node("extract_html_schema", extract_html_schema)
    builder.add_node("check_html_compat", check_html_compatibility)
    builder.add_node("transform_web", transform_web_with_prompt)
    builder.add_node("suggest_css_optimizations", suggest_css_optimizations)
    builder.add_node("refactor_component", refactor_component)
    builder.add_node("log_metadata", log_metadata)

    # Entry point is now the validator
    builder.set_entry_point("validate_input")

    # Add edges conditionally (ASP.NET only path)
    builder.add_edge("validate_input", "extract_html_schema")
    builder.add_edge("extract_html_schema", "check_html_compat")
    builder.add_edge("check_html_compat", "transform_web")
    builder.add_edge("transform_web", "suggest_css_optimizations")
    builder.add_edge("suggest_css_optimizations", "refactor_component")
    builder.add_edge("refactor_component", "log_metadata")

    # Compile and run the graph pipeline
    graph = builder.compile()
    return graph.invoke({"input": html_code, "output": ""})
