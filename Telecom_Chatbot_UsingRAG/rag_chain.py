# -------------------Project: Telecom Chatbot Using RAG - Rag Chain----------------------------
# This file builds the complete Retrieval-Augmented Generation (RAG) pipeline.
# The pipeline performs the following steps:
#
# 1. Receive the user's question.
# 2. Search multiple knowledge sources using the Retriever.
# 3. Combine all retrieved documents into a single context.
# 4. Send the context and question to the LLM.
# 5. Return the generated answer.
#
# Overall Workflow
#
#                 User Question
#                       │
#                       ▼
#               Multi-Source Retriever
#             (FAQ + Tickets + PDF Guide)
#                       │
#                       ▼
#              Retrieved Relevant Documents
#                       │
#                       ▼
#                  Prompt Template
#                       │
#                       ▼
#                Groq Large Language Model
#                       │
#                       ▼
#                  Final AI Response
#
# -----------------------------------------------------------------------------------
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from langchain_groq import ChatGroq

from retriever import build_retriever

# -------------------System Prompt----------------------------
# The System Prompt defines the AI assistant's role and behavior.
# It tells the LLM:
# • Who it is
# • What information it can use
# • How it should respond
# • What to do when information is unavailable
# This prompt remains constant for every user question.
# -----------------------------------------------------------------------------------

SYSTEM_PROMPT = """You are a helpful and professional telecom customer care assistant.
Your job is to help customers resolve technical issues with their mobile service.

Use ONLY the context below to answer the customer's question.
The context comes from two sources:
- FAQ entries (general policy and how-to information)
- Past support tickets (real resolved cases with step-by-step resolutions)

If the context does not contain enough information to answer confidently, say so clearly \
and suggest the customer call 611 or use the MyTelecom app.

Context:
{context}
"""


def _format_docs(docs: list[Document]) -> str:
# ----------Converts the retrieved LangChain Document objects into plain text--------------
# Why is this required?
# The Retriever returns a list of Document objects like:
# [
#     Document(...),
#     Document(...),
#     Document(...)
# ]
#
# Large Language Models (LLMs) cannot directly understand Python objects.
# They expect plain text as input.
# Therefore, we extract the page_content from each Document and format it
# into a readable text block before sending it to the LLM.
#
# Example Output:
# -------------------------------------------------
# [FAQ]
#
# Q: How do I activate roaming?
# A: Open the MyTelecom App and enable roaming.
# -------------------------------------------------
#
# [TICKET]
# Issue: No Internet
# Resolution: Reset APN settings and restart the phone.
# -------------------------------------------------
# The formatted text becomes the {context} variable inside the prompt that
# is finally sent to the LLM.
# ------------------------------------------------------------------------------
    sections = []
    for doc in docs:
        source = doc.metadata.get("source", "unknown").upper()
        sections.append(f"[{source}]\n{doc.page_content}")
    return "\n\n---\n\n".join(sections)


def build_chain():
    # --------------------Step 1 - Build Retriever----------------------------
    # The retriever searches:
    # • FAQ Collection
    # • Ticket Collection
    # • PDF Guide Collection
    # and returns the most relevant documents.
    # --------------------------------------------------------------------------

    retriever = build_retriever()

    # ----------------Step 2 - Create Prompt Template---------------------------
    # The prompt contains:
    # System Message
    #     ↓
    # Instructions for the AI
    #
    # Human Message
    #     ↓
    # Actual user question
    #
    # LangChain automatically replaces:
    #
    # {context}
    # with retrieved documents.
    # --------------------------------------------------------------------------
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{question}"),
    ])
    # -----------------Step 3 - Configure the LLM-------------------------
    # We use Groq's hosted Llama model.
    # Temperature = 0
    # gives deterministic and consistent answers, which is ideal for customer support applications.
    # --------------------------------------------------------------------------
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        max_tokens=None,
        # reasoning_format="parsed",
        timeout=None,
        max_retries=2,
    )

    # ---------------Step 4 - Build the LangChain Pipeline-----------------------
    # Pipeline Flow
    # Question → Retriever → Context → Prompt → LLM → Answer
    # --------------------------------------------------------------------------

    chain = (
        {"context": retriever | _format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain