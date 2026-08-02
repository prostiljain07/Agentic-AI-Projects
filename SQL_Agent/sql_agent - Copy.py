# -----------------Project: SQL Agent || File: sql_agent.py--------------------------------------------------
# This file builds the SQL Agent by combining:
#
#   • Groq Large Language Model (LLM)
#   • Database Tools
#   • System Prompt
#
# The SQL Agent can understand natural language questions, decide which tools
# to use, generate SQL queries, execute them, and explain the results.
#
# Workflow: 
#    User Question
#        │
#        ▼
#     SQL Agent
#        │
#        ▼
#   Uses Database Tools
#        │
#        ▼
#    Executes SQL
#        │
#        ▼
#    Returns Answer
# -----------------------------------------------------------------------------------

from dotenv import load_dotenv
from langchain.agents import create_agent
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from tools import (
    list_tables,
    get_schema,
    execute_sql
)
from prompts import SYSTEM_PROMPT

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)


# Create SQL Agent
sql_agent = create_agent(
    model=llm,
    tools=[
        list_tables,
        get_schema,
        execute_sql
    ],
    system_prompt=SYSTEM_PROMPT
)


# Test Agent
if __name__ == "__main__":
    question = "Average order value."
    result = sql_agent.invoke(
        {
            "messages":[
                {
                    "role":"user",
                    "content":question
                }
            ]
        }
    )

    print(result["messages"][-1].content)