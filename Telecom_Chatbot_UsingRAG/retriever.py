# ------------------------Project: Telecom Chatbot Using RAG - Retriever-----------------------------------
# This script builds a Retriever that searches across THREE different Chroma
# collections:#
#   1. FAQ Collection
#   2. Resolved Support Tickets
#   3. Telecom User Guide (PDF)
#
# Why?
# Instead of searching only one knowledge source, we search all three sources
# simultaneously. This allows the chatbot to provide richer and more accurate
# answers.
# Example:- User asks: "My mobile data is not working after roaming."
# Retriever searches:
# FAQ Collection
#      ↓
# Roaming settings
#
# Ticket Collection
#      ↓
# Previous customer resolution
#
# PDF Guide
#      ↓
# Technical troubleshooting steps
#
# All retrieved documents are merged and sent to the LLM.
# -----------------------------------------------------------------------------------
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.runnables import RunnableLambda
from langchain_core.documents import Document

CHROMA_DIR  = "chroma_store"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def build_retriever(
    k_faq: int = 3,
    k_tickets: int = 3,
    k_guides: int = 3,
) -> RunnableLambda:
    # ----------------Step 1 - Load Embedding Model---------------------------
    # The user's question will be converted into an embedding before searching
    # the vector database.
    # The same embedding model must match the one used while creating the vectors.
    # --------------------------------------------------------------------------
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    # -----------------Step 2 - Connect to Chroma Collections---------------------
    # We already created these collections during the ingestion step:
    # "faq", "tickets", and "guides".    #
    # Here we simply reconnect to them.
    # --------------------------------------------------------------------------
    faq_store = Chroma(
        collection_name="faq",
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )
    tickets_store = Chroma(
        collection_name="tickets",
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )
    guides_store = Chroma(
        collection_name="guides",
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )

    # ---------------------Step 3 - Create Retrievers----------------------------
    # A Retriever is responsible for searching the vector database.
    # search_kwargs={"k":3}
    # means:
    # Return the Top 3 most similar documents.
    # --------------------------------------------------------------------------

    faq_retriever     = faq_store.as_retriever(search_kwargs={"k": k_faq})
    tickets_retriever = tickets_store.as_retriever(search_kwargs={"k": k_tickets})
    guides_retriever  = guides_store.as_retriever(search_kwargs={"k": k_guides})

    # -------------------Step 4 - Merge Results--------------------------
    # Every retriever searches independently.
    # Example
    # User Question: "How do I activate roaming?"
    #
    # FAQ Retriever
    # ----------------
    # FAQ 12
    # FAQ 18
    # FAQ 21
    #
    # Ticket Retriever
    # ----------------
    # Ticket 52
    # Ticket 84
    # Ticket 90
    #
    # Guide Retriever
    # ----------------
    # Chunk 44
    # Chunk 45
    # Chunk 46
    #
    # Final Result:  9 documents returned to the LLM
    # --------------------------------------------------------------------------
    def retrieve(query: str) -> list[Document]:
        return (
            faq_retriever.invoke(query)
            + tickets_retriever.invoke(query)
            + guides_retriever.invoke(query)
        )

    # ------------------Step 5 - Convert to LangChain Runnable------------------------
    # RunnableLambda allows this function to become part of a LangChain pipeline.
    # Later the chain will look like:
    #
    # User Question
    #        │
    #        ▼
    # Retriever
    #        │
    #        ▼
    # Prompt
    #        │
    #        ▼
    # LLM
    #        │
    #        ▼
    # Final Answer
    # --------------------------------------------------------------------------
    return RunnableLambda(retrieve)