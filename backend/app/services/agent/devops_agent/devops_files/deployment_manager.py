from typing import List
from .devops_types import DevOpsState
from .logger_config import setup_logger


# Load environment variables
logger = setup_logger("DevOpsLogger")

def recommend_deployment_strategy(state: DevOpsState) -> DevOpsState:
    """
    Appends deployment strategy recommendations to the DevOps output
    based on detected technologies or keywords.

    Args:
        state (DevOpsState): Current pipeline state containing CI/CD script and metadata.

    Returns:
        DevOpsState: Updated state with appended deployment strategy recommendations.
    """
    try:
        jenkins_script = state.Devops_output
        recommendations: List[str] = []

        # Check for DockerHub usage
        if "dockerhub" in jenkins_script.lower():
            recommendations.append(
                "# Deployment Strategy Tip: Use Docker tags and automated builds in DockerHub. "
                "Integrate Jenkins with DockerHub webhooks to trigger builds and deployments on image push."
            )

        # Check for Kubernetes usage
        if "kubernetes" in jenkins_script.lower():
            recommendations.append(
                "# Kubernetes Deployment Tip: Use Rolling Updates or Blue/Green deployment strategies "
                "with readiness probes for zero-downtime deployments."
            )

        # Generic CI/CD practices
        if "pipeline" in jenkins_script.lower() or "jenkins" in jenkins_script.lower():
            recommendations.append(
                "# CI/CD Tip: Automate your deployment process with stages like Build, Test, and Deploy. "
                "Use proper error handling and post-build actions to ensure stability."
            )

        # Append suggestions if any
        if recommendations:
            annotated_script = "\n\n# -- Deployment Strategy Recommendations --\n" + "\n".join(recommendations)
            state.Devops_output += annotated_script
            logger.info("Appended deployment strategy recommendations to Devops_output.")

        return state

    except Exception as e:
        logger.error(f"Error while recommending deployment strategy: {str(e)}")
        raise