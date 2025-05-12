import json
from datetime import datetime
from .devops_types import DevOpsState
from .logger_config import setup_logger

logger = setup_logger("DevOpsLogger")

def validate_state(state: DevOpsState) -> bool:
    return bool(state.Devops_input and state.Devops_output)

def log_metadata(state: DevOpsState) -> DevOpsState:
    """
    Logs metadata specific to the DevOps transformation process.

    Args:
        state (DevOpsState): Pipeline state with input and output code.

    Returns:
        DevOpsState: The same state, after logging.
    """
    if not validate_state(state):
        logger.warning("Invalid state object. Missing required fields.")
        return state

    try:
        log_data = {
            "procedure_name": "devops_transform_infra",
            "original_code": state.Devops_input,
            "converted_code": state.Devops_output,
            "compatibility_flags": [],
            "optimization_suggestions": [],
            "comments": "",
            "timestamp": datetime.utcnow().isoformat(),
            "status": "success"
        }

        logger.info("===== DEVOPS AGENT FINAL OUTPUT =====")
        logger.info(json.dumps(log_data, indent=2))

    except Exception as e:
        logger.error("Error while logging DevOps metadata", exc_info=True)

    return state