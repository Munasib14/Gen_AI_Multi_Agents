def check_tsql_compatibility(state: dict) -> dict:
    sql_text = state["input"]

    flags = []
    if "raiserror" in sql_text.lower():
        flags.append("RAISERROR is deprecated in Azure SQL. Use THROW instead.")

    state["output"] += "\n-- Compatibility Flags: " + ", ".join(flags)
    return state