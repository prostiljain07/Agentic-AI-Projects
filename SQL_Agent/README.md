# 📊 SQL Agent

This project is a simple AI assistant that lets you ask questions about a retail sales database using plain English.

Instead of writing SQL yourself, you can type questions like:

- How many customers are there?
- List all electronics products.
- What is the top 10 customers by spending?
- Show revenue by product category.

The app turns your question into SQL, runs it against a SQLite database, and then explains the result in simple business language.

## ✨ What this project does

The SQL Agent helps you:

- understand your database structure
- generate safe SQL queries
- run queries on a local SQLite database
- get a human-friendly explanation of the results

It is useful for beginners who want to learn how AI can work with databases.

## 🧠 How it works

1. You type a question in normal language.
2. The app reads the database schema.
3. The AI model creates a safe SQLite query.
4. The query is run against the local database.
5. The results are shown in the app and explained in simple words.

This makes it easier to explore data without manually writing SQL.

## 📁 Folder structure

```text
SQL_Agent/
├── app.py                 # Streamlit web app
├── sql_agent.py           # Main logic for SQL generation and explanation
├── tools.py               # Helper functions for database access
├── prompts.py             # Prompt instructions for the AI agent
├── create_database.py     # Creates the SQLite sample database
├── data/
│   └── sales.db           # Sample retail sales database
├── test.py                # Small test script
└── sql_agent - Copy.py    # Backup copy of the main script
```

## ✅ Requirements

Make sure you have:

- Python installed
- A Groq API key
- Internet access for the AI model

## ▶️ Setup steps

### 1. Install dependencies

From the workspace root, install the required packages:

```bash
pip install -r requirements.txt
```

If you are already inside the SQL_Agent folder, you can also use:

```bash
pip install -r ../requirements.txt
```

### 2. Create a .env file

Create a file named .env in the SQL_Agent folder and add your Groq API key:

```bash
GROQ_API_KEY=your_api_key_here
```

### 3. Create the database

Run this command once to build the sample SQLite database:

```bash
python create_database.py
```

### 4. Run the app

Start the Streamlit app:

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

## 💬 Example questions

Try asking things like:

- How many customers are there?
- Show me the latest 20 orders.
- Which products are never sold?
- What is the average product price?
- Top 5 cities by sales.

## ⚠️ Notes for beginners

- The first run may take a little time because the model needs to load.
- If the app shows an error, check your API key and your internet connection.
- The app only uses safe SELECT queries and does not change the database.

## 📌 Summary

This project is a beginner-friendly example of how AI can be connected to a database to answer business questions in natural language.
