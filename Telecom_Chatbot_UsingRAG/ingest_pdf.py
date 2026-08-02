# ---------------------Project: Telecom Chatbot Using RAG - Ingest PDF------------------------------------
# This script reads a Telecom User Guide PDF, splits it into smaller chunks,
# converts each chunk into vector embeddings, and stores them in a Chroma
# vector database.
# Why?
# Large Language Models (LLMs) have context size limitations. Instead of giving
# the entire PDF to the model every time, we split it into smaller pieces,
# generate embeddings, and store them in Chroma.
# During a user query:
#     User Question
#            │
#            ▼
#   Convert question to embedding
#            │
#            ▼
#   Search Chroma for similar chunks
#            │
#            ▼
#   Send only the relevant chunks to the LLM
# This makes the chatbot faster, cheaper, and more accurate.
# -----------------------------------------------------------------------------------
import os
from pathlib import Path
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

CHROMA_DIR = "chroma_store"
COLLECTION = "guides"
BASE_DIR = Path(__file__).resolve().parent
PDF_PATH = BASE_DIR / "data" / "telecom_guide.pdf"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

CHUNK_SIZE    = 600
CHUNK_OVERLAP = 100

def main():
    # ---------------Step 1 - Load the PDF-------------------------------------
    # PyPDFLoader reads the PDF and converts each page into a LangChain
    # Document object.
    # Example:
    # Page 1  ---> Document
    # Page 2  ---> Document
    # Page 3  ---> Document
    # --------------------------------------------------------------------------
    print("Loading PDF...")
    loader = PyPDFLoader(PDF_PATH)
    pages = loader.load()
    print(f"  {len(pages)} pages loaded.")

    # ---------------Step 2 - Split the PDF into Chunks-------------------------
    # Why split the document?
    # Large Language Models cannot efficiently process very large documents.
    # Example:
    # Original PDF
    # -------------------------
    # 50 Pages
    # becomes  Chunk 1, Chunk 2, Chunk 3, ..., Chunk N    # Chunk 2
    # During retrieval, only the most relevant chunks are sent to the LLM.
    # --------------------------------------------------------------------------
    print(f"Chunking (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " "],
    )
    chunks = splitter.split_documents(pages)

    # ---------------Step 3 - Add Metadata--------------------------------------
    # Metadata helps identify where each chunk came from.
    # Example:
    # {
    #     "source": "guide",
    #     "chunk_index": 15
    # }
    # This information is useful for debugging and citations.
    # --------------------------------------------------------------------------

    for i, chunk in enumerate(chunks):
        chunk.metadata["source"] = "guide"
        chunk.metadata["chunk_index"] = i

    print(f"  {len(chunks)} chunks produced.")

    # ----------------Step 4 - Load Embedding Model------------------------------
    # Embeddings convert text into numerical vectors.
    # Example:
    # "How do I activate roaming?"
    # becomes
    # [0.21, -0.47, 0.81, ....]
    # Similar questions generate similar vectors.
    # --------------------------------------------------------------------------

    print("Initialising embedding model...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    # ----------------Step 5 - Store Embeddings in Chroma------------------------
    # Chroma performs three tasks:
    # 1. Generates embeddings for every chunk.
    # 2. Stores the embeddings.
    # 3. Saves them on disk.
    # Later, when the user asks a question:
    # User Question
    #        │
    #        ▼
    # Convert Question → Embedding
    #        │
    #        ▼
    # Search Chroma
    #        │
    #        ▼
    # Retrieve Top Matching Chunks
    #        │
    #        ▼
    # Send Chunks to LLM
    # --------------------------------------------------------------------------
    print(f"Embedding and storing in Chroma collection '{COLLECTION}'...")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION,
        persist_directory=CHROMA_DIR,
    )
    print(f"  Done. {vectorstore._collection.count()} vectors stored.")


# This code runs only when this file is executed directly.
if __name__ == "__main__":
    main()