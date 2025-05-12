def validate_conversion_input(state: dict) -> dict:
    """
    Validates the input payload for React UI and API conversion workflows.
    Flags missing or malformed structures.
    """
    input_data = state.get("input")
    validation_errors = []

    if not input_data:
        validation_errors.append("Missing 'input' field with React or API code.")

    # Basic check for React component
    # if isinstance(input_data, str):
    #     if "function " not in input_data and "const " not in input_data and "class " not in input_data:
    #         validation_errors.append("Input does not appear to contain a valid React component structure.")
    #     if "return (" not in input_data:
    #         validation_errors.append("React component is missing a return block.")
    #     if "<" not in input_data or ">" not in input_data:
    #         validation_errors.append("No JSX found in input; is this a valid React component?")
    
    # Check for API route format
    if "app.get(" in input_data or "app.post(" in input_data:
        if "res.send" not in input_data and "res.json" not in input_data:
            validation_errors.append("API route detected but missing response logic (res.send or res.json).")

    state["validation_errors"] = validation_errors
    if validation_errors:
        state["output"] += "\n# Validation Errors: " + ", ".join(validation_errors)
    return state