from typing import List
from pydantic import BaseModel, Field

from .logger_config import setup_logger
logger = setup_logger("DevOpsLogger")

class DevOpsState(BaseModel):
    Devops_input: str
    Devops_output: str = ""
    gh_token: str
    gh_repo: str
    logs: List[str] = Field(default_factory=list)
    github_status: str = ""
    gh_file_path: str = ".github/workflows/generated_pipeline.yml"
    gh_branch: str = "main"
    gh_commit_msg: str = "Add GitHub Actions workflow"


def refactor_devops(state: DevOpsState) -> DevOpsState:
    """
    Analyzes DevOps infrastructure code and appends refactoring suggestions
    for improved modularity, maintainability, and DevOps best practices.

    Args:
        state (DevOpsState): The current DevOps state containing input code and metadata.

    Returns:
        DevOpsState: Updated state with appended refactoring suggestions.
    """
    try:
        comments = []

        input_code = state.Devops_input.lower()

        if "resource" in input_code:
            comments.append("# Consider splitting resources into reusable modules.")

        if "aws_instance" in input_code:
            comments.append("# Use variables for AMI ID and instance type to improve flexibility.")

        if "jenkins" in input_code:
            comments.append("# Follow naming conventions and folder structure for Jenkins pipelines.")

        # Always append a general best practice comment
        comments.append("# Keep secrets and sensitive data in environment variables or secrets manager.")

        if comments:
            state.Devops_output += "\n\n# -- Refactoring Suggestions --\n" + "\n".join(comments)
            logger.info(f"Added {len(comments)} refactoring suggestion(s).")

    except Exception as e:
        logger.exception("Failed to generate refactoring suggestions.")
        state.logs.append(f"Error during refactor_devops: {e}")

    return state