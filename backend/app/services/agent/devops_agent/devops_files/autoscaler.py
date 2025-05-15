from typing import List
from .devops_types import DevOpsState
from .logger_config import setup_logger

logger = setup_logger("DevOpsLogger")

def suggest_jenkins_optimizations(state: DevOpsState) -> DevOpsState:
    """
    Analyzes a Jenkins pipeline script and appends optimization suggestions to the Devops_output field.

    Args:
        state (DevOpsState): The current pipeline transformation state.

    Returns:
        DevOpsState: Updated state with optimization suggestions appended to Devops_output.
    """
    try:
        jenkins_script = state.Devops_output
        suggestions: List[str] = []

        # Optimization checks
        if "agent any" in jenkins_script.lower():
            suggestions.append("Consider specifying a more granular agent label instead of 'any' to optimize resource usage.")
        
        if "sh './gradlew" in jenkins_script and "parallel" not in jenkins_script:
            suggestions.append("Consider using parallel stages to speed up build and test processes.")
        
        if "post {" not in jenkins_script.lower():
            suggestions.append("Include a 'post' section for better visibility into pipeline success or failure.")
        
        if "parameters {" not in jenkins_script.lower():
            suggestions.append("Use parameters to make the pipeline reusable for different environments or builds.")

        # Append suggestions to output
        if suggestions:
            formatted_suggestions = "\n".join(f"// - {s}" for s in suggestions)
            state.Devops_output += (
                "\n\n// -- Jenkins Pipeline Optimization Suggestions --\n" +
                formatted_suggestions
            )
            logger.info("Jenkins optimizations suggested:\n%s", formatted_suggestions)
        else:
            logger.info("No Jenkins optimizations suggested.")

    except Exception as e:
        logger.error("Error while suggesting Jenkins optimizations", exc_info=True)

    return state
