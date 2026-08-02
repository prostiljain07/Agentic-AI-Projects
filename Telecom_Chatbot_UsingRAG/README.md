# 📡 Telecom Customer Care Chatbot

This project is a simple chatbot for a telecom company. It can answer questions about mobile service, billing, roaming, SIM issues, internet problems, and more.

The chatbot uses a technique called RAG (Retrieval-Augmented Generation). In simple words, it first searches through saved support information, then uses that information to answer your question.

## ✨ What this project does

You can ask questions like:

- Why is my internet slow?
- Why are my calls dropping?
- How do I activate roaming?
- Why is my bill higher than usual?

The bot tries to give helpful answers based on the knowledge stored in the project.

## 📁 Main files

- app.py: the web app built with Streamlit
- rag_chain.py: connects the search system to the language model
- retriever.py: finds the best matching information from the saved data
- ingest_faq.py: loads FAQ data into the search database
- ingest_tickets.py: loads resolved support tickets into the search database
- ingest_pdf.py: loads a PDF guide into the search database

## ✅ Requirements

Before starting, make sure you have:

- Python installed
- A Groq API key
- Internet access to download the models and packages

## ▶️ Step 1: Install the packages

Open your terminal and go to the workspace root, then install the packages:

```bash
pip install -r requirements.txt
```

If you are already inside this project folder, you can use:

```bash
pip install -r ../requirements.txt
```

## 🔐 Step 2: Create a .env file

Create a file named .env in this folder and add your Groq API key:

```bash
GROQ_API_KEY=your_api_key_here
```

## 🧠 Step 3: Build the knowledge base

This step loads the FAQ, ticket data, and PDF guide into the search database.

Run these commands:

```bash
python ingest_faq.py
python ingest_tickets.py
python ingest_pdf.py
```

These scripts may take some time the first time because they download models.

## 🚀 Step 4: Run the chatbot

To start the web app:

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

You can also run a simple terminal version:

```bash
python main_Testing.py
```

## 🛠️ How it works

1. You ask a question.
2. The app searches the saved FAQ, ticket history, and PDF guide.
3. It finds the most relevant information.
4. The AI model uses that information to write a helpful answer.

This is why the bot can answer questions more accurately than a normal chatbot that does not use extra knowledge.

## 💬 How to use it

- Type your question in the chat box
- Click one of the sample questions on the left side
- The bot will search the saved support information and reply

## ⚠️ Troubleshooting

- If the app does not start, make sure you installed the packages correctly.
- If you see an API error, check that your Groq API key is valid and placed in the .env file.
- If the bot gives weak answers, try re-running the data ingestion scripts so the latest knowledge is loaded.
- If the app is slow, it is usually because the model is downloading or loading for the first time.

## 🌱 Notes for beginners

- The first run may take a few minutes
- If the bot says it does not know the answer, it may mean the stored data does not contain enough information
- Keep your API key safe and do not share it publicly

## 📌 Summary

This project is a beginner-friendly example of a smart chatbot that uses search + AI to answer telecom support questions.
