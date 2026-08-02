# -----------------Project: SQL Agent || File: app.py----------------------------------------------------
# Streamlit application for interacting with the SQL AI Agent.
#
# Features
# --------
# • ChatGPT-style interface
# • Conversation history
# • Displays Generated SQL
# • Displays Query Results
# • AI Business Explanation
# • Clear Chat
# -----------------------------------------------------------------------------------

import streamlit as st
from sql_agent import ask_database

st.set_page_config(
    page_title="SQL AI Assistant",
    page_icon="📊",
    layout="wide"
)

with st.sidebar:
    st.title("📊 SQL AI Assistant")
    st.markdown("---")
    st.markdown("### Database")
    st.success("Retail Sales Database")
    st.markdown("---")
    st.markdown("### Example Questions")
    examples = [
        "How many customers are there?",
        "List all Electronics products.",
        "Top 10 customers by spending.",
        "Revenue by category.",
        "Average product price.",
        "Show the latest 20 orders.",
        "Products never sold.",
        "Top 5 cities by sales."
    ]

    for q in examples:
        st.write("•", q)
    st.markdown("---")
    if st.button("🗑 Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

st.title("🤖 SQL AI Assistant")

st.caption(
    "Ask questions about your Retail Sales Database using natural language."
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(chat["question"])
    with st.chat_message("assistant"):
        st.markdown("### 📝 Generated SQL")
        st.code(chat["sql"], language="sql")
        st.markdown("### 📊 Query Results")
        st.dataframe(chat["data"], use_container_width=True)
        st.markdown("### 🤖 AI Explanation")
        st.write(chat["answer"])

question = st.chat_input("Ask your business question...")

if question:
    with st.chat_message("user"):
        st.markdown(question)
    
    with st.chat_message("assistant"):
        with st.spinner("Generating SQL and analysing data..."):
            try:
                result = ask_database(question)
                st.markdown("### 📝 Generated SQL")
                st.code(result["sql"], language="sql")
                st.markdown("### 📊 Query Results")
                st.dataframe(
                    result["data"],
                    use_container_width=True
                )
                st.markdown("### 🤖 AI Explanation")
                st.write(result["answer"])
                st.session_state.chat_history.append(
                    {
                        "question": question,
                        "sql": result["sql"],
                        "data": result["data"],
                        "answer": result["answer"]
                    }
                )
            except Exception as e:
                st.error(str(e))