import re
from typing import List
from .devops_types import DevOpsState
from .logger_config import setup_logger
from typing import List


# Load environment variables
logger = setup_logger("DevOpsLogger")


# Constants for log levels
INFO = "INFO"
WARNING = "WARNING"
ERROR = "ERROR"

def _log_issue(state: DevOpsState, level: str, code: str, message: str) -> None:
    """
    Appends a structured issue to the DevOpsState logs and logs it.
    """
    log_entry = f"[{level}] {code}: {message}"
    state.logs.append(log_entry)

    if level == INFO:
        logger.info(log_entry)
    elif level == WARNING:
        logger.warning(log_entry)
    elif level == ERROR:
        logger.error(log_entry)

def _check_pattern(state: DevOpsState, code: str, pattern: str, code_name: str, success_msg: str, failure_msg: str) -> bool:
    """
    Checks for a regex pattern and returns match status while providing logs.
    """
    if re.search(pattern, code, re.IGNORECASE):
        _log_issue(state, INFO, code_name, success_msg)
        return True
    else:
        _log_issue(state, WARNING, code_name, failure_msg)
        return False

def terraform_linter(state: DevOpsState) -> DevOpsState:
    """
    Lints Terraform code to detect missing blocks and provide guidance for best practices.
    """
    code = state.Devops_input
    if not isinstance(code, str) or not code.strip():
        _log_issue(state, ERROR, "TERRAFORM_EMPTY", "No valid Terraform input provided.")
        return state

    try:
        # Run checks
        _check_pattern(code, r'\bresource\b', "TERRAFORM_RESOURCE", 
                       "'resource' block detected.", 
                       "Missing 'resource' block.")

        _check_pattern(code, r'\bprovider\b', "TERRAFORM_PROVIDER", 
                       "'provider' block detected.", 
                       "Missing 'provider' block. Required for cloud deployment.")

        _check_pattern(code, r'\bvariable\b', "TERRAFORM_VARIABLE", 
                       "'variable' blocks detected.", 
                       "No variables found. Use variables for flexibility.")

        _check_pattern(code, r'\baws_', "TERRAFORM_AWS", 
                       "AWS-specific resources found.", 
                       "No AWS resources detected.")

        logger.info("Terraform linter completed successfully.")

    except Exception as e:
        _log_issue(state, ERROR, "TERRAFORM_LINTER_EXCEPTION", f"Unexpected error during linting: {str(e)}")

    return state



def terraform_plan_validator(state: DevOpsState) -> DevOpsState:
    """
    Validates Terraform configuration for key components and best practices.

    Args:
        state (DevOpsState): The current state object containing DevOps input.

    Returns:
        DevOpsState: The updated state with validation logs.
    """
    code: str = state.Devops_input or ""
    logs: List[str] = []

    logger.info("Starting Terraform plan validation.")

    # Check for EC2 resource
    if "aws_instance" in code:
        logs.append("Terraform Plan Validator: ✅ EC2 instance resource defined.")
    else:
        logs.append("Terraform Plan Validator: ⚠️ No EC2 resource found.")

    # Check for provider block
    if "provider" not in code:
        logs.append("Terraform Plan Validator: ⚠️ Missing 'provider' block.")

    # Check for required fields
    required_fields = ["ami", "instance_type"]
    for field in required_fields:
        if field not in code:
            logs.append(f"Terraform Plan Validator: ⚠️ Missing required EC2 field: '{field}'")

    # Add logs to state and complete
    state.logs.extend(logs)
    logger.info("Terraform plan validation completed successfully.")

    return state
