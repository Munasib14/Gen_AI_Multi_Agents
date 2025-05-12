def refactor_procedure(state: dict) -> dict:
    sql_text = state["input"]
    comments = []

    if "begin" in sql_text.lower():
        comments.append("-- Ensure BEGIN/END blocks are scoped properly")
    
    comments.append("-- Use TRY/CATCH for better error handling")

    state["output"] += "\n-- Refactoring Comments --\n" + "\n".join(comments)
    return state