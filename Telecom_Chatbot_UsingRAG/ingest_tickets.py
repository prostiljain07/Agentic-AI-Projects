# ------------------Project: Telecom Chatbot Using RAG---------------------------------
# This script reads resolved customer support tickets stored in a SQLite database,
# converts each ticket into a LangChain Document, generates vector embeddings,
# and stores them in a Chroma vector database.
# Why?
# Real customer support tickets contain practical solutions to common issues.
# Instead of training an LLM on these tickets, we convert them into embeddings
# and store them in a vector database.
# During a customer conversation:
#       User Question
#             │
#             ▼
#   Convert question to embedding
#             │
#             ▼
#   Search Chroma for similar tickets
#             │
#             ▼
#   Retrieve previous resolutions
#             │
#             ▼
#   Provide an informed response to the user
# This enables Retrieval-Augmented Generation (RAG).
# -----------------------------------------------------------------------------------
import os
from pathlib import Path
import sqlite3
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
import pandas as pd
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

CHROMA_DIR = "chroma_store"
COLLECTION  = "tickets"
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "tickets.db"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def load_ticket_documents(db_path: str) -> list[Document]:
    """
    Reads resolved support tickets from the SQLite database and converts
    each ticket into a LangChain Document.
    Input:
        db_path -> Path of the SQLite database.

    Output:
        List of LangChain Document objects.

    Why use only resolved tickets?
    ------------------------------
    We only want to retrieve successful solutions.
    Open or unresolved tickets would provide incomplete or incorrect answers.

    Example Document

    page_content:

        Issue: Network Issue
        Description: Customer has no mobile data.
        Resolution: Reset APN settings and restart the phone.

    metadata:

        {
            "source": "ticket",
            "ticket_id": 1056,
            "category": "Network",
            "status": "resolved"
        }
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM tickets WHERE status = 'resolved'"
    ).fetchall()
    conn.close()

    docs = []
    for row in rows:
        # Combine issue description + resolution into a single searchable text block
        content = (
            f"Issue: {row['issue_type']}\n"
            f"Description: {row['description']}\n"
            f"Resolution: {row['resolution']}"
        )
        docs.append(Document(
            page_content=content,
            metadata={
                "source":    "ticket",
                "ticket_id": row["ticket_id"],
                "category":  row["category"],
                "status":    row["status"],
            },
        ))
    return docs


def main():
    # ------------------Step 1 - Load Ticket Documents-------------------------
    # Read all resolved support tickets from the SQLite database.
    # Example:
    # Ticket 1 ---> Document
    # Ticket 2 ---> Document
    # Ticket 3 ---> Document
    # --------------------------------------------------------------------------
    print("Loading ticket documents from SQLite...")
    docs = load_ticket_documents(DB_PATH)
    print(f"  {len(docs)} resolved tickets loaded.")

    # ------------------Step 2 - Load Embedding Model-------------------------
    # Embeddings convert text into numerical vectors.
    # Example:
    # "Customer cannot access mobile data."
    # becomes
    # [0.12, -0.41, 0.87, ...]
    # Similar problems generate similar vectors.
    # --------------------------------------------------------------------------    
    print("Initialising embedding model...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    # ------------------Step 3 - Store Embeddings in Chroma-------------------------
    # Chroma performs three important tasks:
    # 1. Converts every ticket into an embedding.
    # 2. Stores the embeddings.
    # 3. Saves them on disk.
    # Later during chatbot execution:
    # User Question
    #        │
    #        ▼
    # Convert Question → Embedding
    #        │
    #        ▼
    # Search Ticket Collection
    #        │
    #        ▼
    # Retrieve Similar Resolved Tickets
    #        │
    #        ▼
    # Send Results to the LLM
    # This allows the chatbot to answer using previous real-world solutions.
    # --------------------------------------------------------------------------
    print(f"Embedding and storing in Chroma collection '{COLLECTION}'...")
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name=COLLECTION,
        persist_directory=CHROMA_DIR,
    )
    print(f"  Done. {vectorstore._collection.count()} vectors stored.")

# This block executes only when this file is run directly.
if __name__ == "__main__":
    main()