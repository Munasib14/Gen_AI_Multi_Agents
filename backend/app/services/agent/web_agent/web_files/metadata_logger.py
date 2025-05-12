import logging

# Set up a logger
logger = logging.getLogger("WebAgentLogger")
logger.setLevel(logging.INFO)
if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

def log_metadata(state: dict) -> dict:
    """
    Logs metadata for the Web Agent transformation process.
    """
    html_code = state.get("input", "")
    transformed_code = state.get("output", "")
    compatibility_issues = state.get("compatibility_issues", [])
    optimizations = state.get("css_optimizations", [])

    logger.info("===== WEB AGENT FINAL OUTPUT =====")
    logger.info(f"Original HTML Code:\n{html_code}")
    logger.info(f"Transformed React Code:\n{transformed_code}")
    logger.info(f"Compatibility Issues: {compatibility_issues}")
    logger.info(f"CSS Optimizations Suggested: {optimizations}")

    return state
