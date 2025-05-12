import json
from datetime import datetime

def log_metadata(state: dict) -> dict:
    # Extract all info from the state
    final_log = {
        "procedure_name": "usp_get_customers",
        "original_code": state["input"],
        "converted_code": state["output"],
        "compatibility_flags": [],  
        "optimization_suggestions": [],
        "comments": "",
        "timestamp": str(datetime.now()),
        "status": "success"
    }

    # Print final output (you can write to a file if needed)
    print("\n===== DB AGENT FINAL OUTPUT =====\n")
    print(json.dumps(final_log, indent=2))

    return state