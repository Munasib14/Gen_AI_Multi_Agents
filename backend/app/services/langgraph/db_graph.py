from typing import TypedDict
from langgraph.graph import StateGraph

# imports from sibling 'agent' folder
from backend.app.services.agent.db_agent.db_files.schema_extractor import extract_schema
from backend.app.services.agent.db_agent.db_files.validator import check_tsql_compatibility
from backend.app.services.agent.common_files.transformer  import transform_sql
from backend.app.services.agent.db_agent.db_files.performance_tuner import suggest_optimizations
from backend.app.services.agent.db_agent.db_files.refactor_sp import refactor_procedure
from backend.app.services.agent.db_agent.db_files.metadata_logger import log_metadata
from backend.app.services.agent.common_files.prompt_engine import load_db_prompt


# Define shared LangGraph state
class DBState(TypedDict):
    input: str
    output: str


# Main DB Agent orchestration function
def db_agent_main(sql_code: str, prompt_name: str = "transform_identity.j2") -> DBState:
    """
    Executes the DB Agent LangGraph with dynamic prompt support.

    Args:
        sql_code (str): Input SQL string to analyze and transform.
        prompt_name (str): Name of the Jinja2 prompt template to use (default is 'transform_identity.j2').

    Returns:
        DBState: Dictionary with both input and LLM-transformed output.
    """

    # Transformer step with dynamic prompt injection
    def transform_sql_with_prompt(state: DBState) -> DBState:
        return transform_sql(state, prompt_template=prompt_name)

    # Create LangGraph and add nodes
    builder = StateGraph(DBState)

    builder.add_node("extract_schema", extract_schema)
    builder.add_node("check_compat", check_tsql_compatibility)
    builder.add_node("transform_sql", transform_sql_with_prompt)
    builder.add_node("suggest_optimizations", suggest_optimizations)
    builder.add_node("refactor_procedure", refactor_procedure)
    builder.add_node("log_metadata", log_metadata)

    # Define execution flow
    builder.set_entry_point("extract_schema")
    builder.add_edge("extract_schema", "check_compat")
    builder.add_edge("check_compat", "transform_sql")
    builder.add_edge("transform_sql", "suggest_optimizations")
    builder.add_edge("suggest_optimizations", "refactor_procedure")
    builder.add_edge("refactor_procedure", "log_metadata")

    # Compile graph and run the pipeline
    graph = builder.compile()
    return graph.invoke({"input": sql_code, "output": ""})