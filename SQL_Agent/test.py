from langchain_groq import ChatGroq

from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

from tools import list_tables, get_schema, execute_sql

print("=" * 50)
print("Tables")
print("=" * 50)

print(list_tables.invoke({}))

print("\n")

print("=" * 50)
print("Schema")
print("=" * 50)

print(get_schema.invoke({"table_name": "customers"}))

print("\n")

print("=" * 50)
print("SQL")
print("=" * 50)

print(
    execute_sql.invoke(
        {
            "query": """
            SELECT product_name, brand, price
            FROM products
            WHERE category='Electronics'
            """
        }
    )
)