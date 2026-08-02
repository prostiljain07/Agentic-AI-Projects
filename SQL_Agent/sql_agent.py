# -----------------Project: SQL Agent || File: sql_agent.py---------------------------------------
# This module converts a user's natural language question into SQL,
# executes the SQL against a SQLite database,
# and uses the LLM to explain the results.
#
# Workflow: 
# User Question
#       │
#       ▼
# Generate SQL (LLM)
#       │
#       ▼
# Validate SQL
#       │
#       ▼
# Execute SQL (SQLite)
#       │
#       ▼
# Explain Results (LLM)
# -----------------------------------------------------------------------------------

import sqlite3
from pathlib import Path
import pandas as pd

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "sales.db"

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

def get_database_schema():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name NOT LIKE 'sqlite_%'
    """)
    tables = [row[0] for row in cursor.fetchall()]
    schema = ""
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()
        schema += f"\nTable: {table}\n"
        for col in columns:
            schema += f"    {col[1]} ({col[2]})\n"
    conn.close()
    return schema


def generate_sql(question):
    schema = get_database_schema()
    prompt = f"""
            You are an expert SQLite developer.
            Below is the database schema.
            {schema}
            Rules

            1. Generate ONLY SQLite SQL.

            2. Never explain anything.

            3. Never use markdown.

            4. Never use ```sql

            5. Return ONLY SQL.

            6. Use only tables and columns from the schema.

            Question

            {question}
            """
    sql = llm.invoke(prompt).content.strip()
    sql = sql.replace("```sql", "").replace("```", "").strip()
    return sql


def validate_sql(sql):
    sql_upper = sql.upper()
    blocked = [
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "TRUNCATE",
        "CREATE"
    ]
    for keyword in blocked:
        if keyword in sql_upper:
            raise ValueError(
                f"Unsafe SQL detected ({keyword})."
            )
    return sql


def execute_sql(sql):
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query(sql, conn)
        return df
    finally:
        conn.close()


def explain_results(question, df):
    prompt = f"""
        Question
        {question}
        Results
        {df.to_string(index=False)}
        Explain the results in simple business language.
        """
    return llm.invoke(prompt).content


def ask_database(question):
    sql = generate_sql(question)
    sql = validate_sql(sql)
    df = execute_sql(sql)
    explanation = explain_results(question, df)
    return {
        "sql": sql,
        "data": df,
        "answer": explanation
    }


if __name__ == "__main__":

    while True:

        print("\n" + "=" * 100)
        question = input("Ask a question (type 'exit' to quit): ")

        if question.lower() == "exit":
            break

        try:

            result = ask_database(question)

            print("\n" + "=" * 100)
            print("GENERATED SQL")
            print("=" * 100)
            print(result["sql"])

            print("\n" + "=" * 100)
            print("QUERY RESULTS")
            print("=" * 100)
            print(result["data"])

            print("\n" + "=" * 100)
            print("AI EXPLANATION")
            print("=" * 100)
            print(result["answer"])

        except Exception as e:

            print("\n❌ ERROR")
            print(e)