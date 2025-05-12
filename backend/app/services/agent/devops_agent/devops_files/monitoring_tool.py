from .devops_types import DevOpsState
from .logger_config import setup_logger
logger = setup_logger("DevOpsLogger")

def suggest_monitoring_integration(state: DevOpsState) -> DevOpsState:
    """
    Suggests monitoring and observability practices for Jenkins or infrastructure code.
    
    Args:
        state (DevOpsState): Current DevOps agent state.
    
    Returns:
        DevOpsState: Updated state with appended monitoring recommendations.
    """
    if not hasattr(state, "Devops_output") or not isinstance(state.Devops_output, str):
        logger.error("Devops_output is missing or not a string.")
        return state

    script = state.Devops_output
    suggestions = []

    try:
        # Infrastructure-level monitoring recommendations
        if "aws_instance" in script or "autoscaling" in script.lower():
            suggestions.append(
                "Consider integrating AWS CloudWatch, Prometheus, or Grafana to monitor EC2 instances and autoscaling behavior."
            )

        # CI/CD monitoring practices
        if "deploy" in script.lower():
            suggestions.append(
                "Add deployment monitoring hooks (e.g., Datadog, New Relic) to track release health and alert on failures."
            )

        if "sh './gradlew test'" in script:
            suggestions.append(
                "Integrate automated test reporting with Jenkins plugins (e.g., JUnit, Allure) or external dashboards."
            )

        # Append to script only if suggestions exist
        if suggestions:
            annotated_block = "\n\n// -- Monitoring & Observability Suggestions --\n" + \
                              "\n".join(f"// - {s}" for s in suggestions)
            state.Devops_output += annotated_block
            logger.info("Monitoring suggestions appended to DevOps output.")
        else:
            logger.info("No monitoring suggestions detected based on the current script.")

    except Exception as e:
        logger.exception(f"Unexpected error during monitoring suggestion: {e}")

    return state