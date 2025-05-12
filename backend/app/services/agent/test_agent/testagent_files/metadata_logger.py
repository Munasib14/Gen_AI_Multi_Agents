import logging

# Set up a logger
logger = logging.getLogger("PlaywrightConverterLogger")
logger.setLevel(logging.INFO)
if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

def log_metadata(state: dict) -> dict:
    """
    Logs metadata for the Playwright feature and step definition generation process.
    """
    source_file = state.get("input", "")
    generated_feature_file = state.get("feature_file", "")
    generated_step_definitions = state.get("step_definitions", "")
    identified_user_flows = state.get("user_flows", [])
    ui_elements_covered = state.get("ui_elements", [])

    logger.info("===== PLAYWRIGHT BDD OUTPUT =====")
    logger.info(f"Source file:\n{source_file}")
    logger.info(f"Generated Feature File:\n{generated_feature_file}")
    logger.info(f"Generated Step Definitions:\n{generated_step_definitions}")
    logger.info(f"Identified User Flows: {identified_user_flows}")
    logger.info(f"UI Elements Covered: {ui_elements_covered}")

    return state