# ---------------------Project: Telecom Chatbot Using RAG - Ingest FAQ------------------------------------
# This script reads FAQ data from a CSV file, converts each FAQ into a LangChain
# Document object, generates vector embeddings, and stores them in a Chroma
# vector database.
#
# Why?
# LLMs cannot efficiently search large documents on their own. By converting
# documents into embeddings and storing them in a vector database, we can retrieve
# the most relevant information during user conversations.
# -----------------------------------------------------------------------------------

import os
from pathlib import Path
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
import pandas as pd
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Get the directory where this Python file is located.
# This makes the code work regardless of where it is executed from.
CHROMA_DIR = "chroma_store"
COLLECTION  = "faq"
BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "data" / "faq.csv"
#CSV_PATH    = os.path.join("data", "faq.csv")
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def load_faq_documents(csv_path: str) -> list[Document]:
    df = pd.read_csv(csv_path)
    docs = []
    for _, row in df.iterrows():
        content = f"Q: {row['question']}\nA: {row['answer']}"
        docs.append(Document(
            page_content=content,
            metadata={"source": "faq", "category": row["category"], "faq_id": str(row["id"])},
        ))
    return docs

def main():
    # Step 1 - Load FAQ Documents
    print("Loading FAQ documents...")
    docs = load_faq_documents(CSV_PATH)
    print(f"  {len(docs)} FAQ entries loaded.")
    
    # ----------Step 2 - Load Embedding Model--------------------------------
    # Embeddings convert text into numerical vectors.
    # Example:
    # "How do I recharge my phone?"
    # becomes
    # [0.12, -0.45, 0.87, ....]
    # These vectors allow semantic similarity search.
    # --------------------------------------------------------------------------
    print("Initialising embedding model...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    # ----------------Step 3 - Store Documents in Chroma------------------------
    # Chroma performs three tasks:
    # 1. Converts every document into an embedding.
    # 2. Stores the embeddings.
    # 3. Saves them on disk for future searches.
    # Later, when the user asks a question:
    # User Question
    #        │
    #        ▼
    # Convert question to embedding
    #        │
    #        ▼
    # Search Chroma
    #        │
    #        ▼
    # Return the most similar FAQ documents
    # --------------------------------------------------------------------------
    print(f"Embedding and storing in Chroma collection '{COLLECTION}'...")
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name=COLLECTION,
        persist_directory=CHROMA_DIR,
    )
    print(f"  Done. {vectorstore._collection.count()} vectors stored.")

# This block runs only when this file is executed directly.
if __name__ == "__main__":
    main()
