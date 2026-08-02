# -----------------Project: SQL Agent || File: tools.py----------------------------------------------------
# This file contains helper functions (tools) that allow the AI Agent to interact
# with the SQLite database.
# The SQL Agent does not access the database directly. Instead, it uses these
# tools to:
#
# 1. View available tables.
# 2. Inspect a table's schema.
# 3. Execute SQL queries.
#
# These functions will later be converted into LangChain Tools so the LLM can
# call them automatically.
#
# Workflow
# User Question
#        │
#        ▼
#   SQL Agent (LLM)
#        │
#        ▼
#   Database Tools
#   ├── list_tables()
#   ├── get_schema()
#   └── execute_sql()
#        │
#        ▼
#     SQLite Database
# -----------------------------------------------------------------------------------

import sqlite3
from pathlib import Path
import pandas as pd
from langchain.tools import tool


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "sales.db"

def get_connection():
    """
    Creates and returns a connection to the SQLite database.
    """
    return sqlite3.connect(DB_PATH)


# Function: List All Tables
@tool
def list_tables() -> str:
    """
    Returns a list of all tables in the database.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            ORDER BY name
        """)
        tables = cursor.fetchall()
        return "\n".join(row[0] for row in tables)
    finally:
        conn.close()


# Function: Get Table Schema
@tool
def get_schema(table_name: str) -> str:
    """
    Returns the schema of the specified table.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        schema = cursor.fetchall()
        if not schema:
            return f"No schema found for table '{table_name}'."
        return "\n".join(
            f"{col[1]} ({col[2]})"
            for col in schema
        )
    finally:
        conn.close()


# Function: Execute SQL Query
@tool
def execute_sql(query: str) -> str:
    """
    Executes a SQLite SELECT query and returns the results.
    """
    conn = get_connection()
    try:
        df = pd.read_sql_query(query, conn)
        if df.empty:
            return "No records found."
        return df.to_string(index=False)

    except Exception as e:
        return f"SQL Error: {e}"
    finally:
        conn.close()


# Test Functions
if __name__ == "__main__":
    print("=" * 60)
    print("Available Tables")
    print("=" * 60)
    print(list_tables())
    print("\n")
    print("=" * 60)
    print("Customers Schema")
    print("=" * 60)
    for column in get_schema("customers"):
        print(column)

    print("\n")
    print("=" * 60)
    print("Sample Query")
    print("=" * 60)

    query = """
    SELECT *
    FROM customers
    LIMIT 5
    """

    print(execute_sql(query))