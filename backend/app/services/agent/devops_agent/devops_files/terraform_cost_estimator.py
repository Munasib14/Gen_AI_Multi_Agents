from typing import List
from .devops_types import DevOpsState
from .logger_config import setup_logger


# Load environment variables
logger = setup_logger("DevOpsLogger")


# Constants for monthly estimated costs (USD)
AWS_INSTANCE_COST = 120
AWS_S3_BUCKET_COST = 30
AWS_RDS_INSTANCE_COST = 100
AWS_LAMBDA_FUNCTION_COST = 10


def terraform_cost_estimator(state: DevOpsState) -> DevOpsState:
    """
    Estimates the monthly cost of Terraform-defined AWS resources.

    Args:
        state (DevOpsState): The current DevOps state containing the Terraform output.

    Returns:
        DevOpsState: Updated state with estimated cost logs.
    """
    logger.info("Starting Terraform cost estimation")

    try:
        code = state.Devops_output.lower()
        estimated_cost = 0
        cost_breakdown: List[str] = []

        if "aws_instance" in code:
            estimated_cost += AWS_INSTANCE_COST
            cost_breakdown.append(f"• aws_instance: ~${AWS_INSTANCE_COST}/month (t2.medium assumed)")

        if "aws_s3_bucket" in code:
            estimated_cost += AWS_S3_BUCKET_COST
            cost_breakdown.append(f"• aws_s3_bucket: ~${AWS_S3_BUCKET_COST}/month (100GB standard storage)")

        if "aws_rds_instance" in code:
            estimated_cost += AWS_RDS_INSTANCE_COST
            cost_breakdown.append(f"• aws_rds_instance: ~${AWS_RDS_INSTANCE_COST}/month (db.t3.micro assumed)")

        if "aws_lambda_function" in code:
            estimated_cost += AWS_LAMBDA_FUNCTION_COST
            cost_breakdown.append(f"• aws_lambda_function: ~${AWS_LAMBDA_FUNCTION_COST}/month (based on usage)")

        if not cost_breakdown:
            warning_msg = "⚠️ No recognizable AWS resources found. Cannot estimate cost."
            cost_breakdown.append(warning_msg)
            logger.warning(warning_msg)

        # Append logs to state
        state.logs.append("Terraform Cost Estimator: Estimated Monthly Cost 💰")
        state.logs.extend(cost_breakdown)
        state.logs.append(f"→ Total Estimated Cost: ~${estimated_cost}/month")

        logger.info("Terraform Cost Estimator completed successfully. Total: $%d", estimated_cost)
        return state

    except Exception as e:
        error_message = f"Terraform cost estimation failed: {str(e)}"
        logger.exception(error_message)
        state.logs.append(f"❌ {error_message}")
        return state
