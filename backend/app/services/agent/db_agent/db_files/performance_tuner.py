def suggest_optimizations(state: dict) -> dict:
    sql_text = state["input"]
    suggestions = []

    if "select *" in sql_text.lower():
        suggestions.append("Avoid SELECT * for better performance.")
    if "cursor" in sql_text.lower():
        suggestions.append("Replace cursors with set-based operations.")

    state["output"] += "\n-- Optimization Suggestions --\n" + "\n".join(suggestions)
    return state