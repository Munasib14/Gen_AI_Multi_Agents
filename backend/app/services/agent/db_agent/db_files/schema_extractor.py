import sqlparse

def extract_schema(input_sql: str):
    # A Sample example - In production use proper SQL metadata extractors
    tables = []
    procedures = []
    sql_text = input_sql["input"]
    for stmt in sqlparse.split(sql_text):

        stmt = stmt.strip().lower()
        if stmt.startswith("create table"):
            tables.append(stmt.split()[2])
        if stmt.startswith("create procedure"):
            procedures.append(stmt.split()[2])
    return {
        "tables": tables,
        "procedures": procedures,
        "raw_sql": input_sql
    }