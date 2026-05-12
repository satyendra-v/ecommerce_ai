import os
from pathlib import Path
from typing import List
import time

# ── DOCUMENT LOADERS ─────────────────────────────────────────────────────────
# LangChain has loaders for virtually every format.
# Each loader returns a list of Document objects: {page_content: str, metadata: dict}
from langchain_community.document_loaders import (
    PyPDFLoader,            # PDF files — splits by page automatically
    Docx2txtLoader,         # Word documents (.docx)
    TextLoader,             # Plain text files
    WebBaseLoader,          # Fetch and parse a web URL
    UnstructuredMarkdownLoader,  # Markdown files
)

# ── TEXT SPLITTER ─────────────────────────────────────────────────────────────
# Why split? LLM context windows are limited. A 100-page PDF can't fit in a prompt.
# We split into chunks of ~500 tokens. Each chunk is stored as a separate vector.
# At query time we retrieve the most relevant chunks, not the whole document.
from langchain_text_splitters import RecursiveCharacterTextSplitter
# RecursiveCharacterTextSplitter is the recommended default.
# It tries to split on paragraph breaks first (\n\n), then sentences (\n),
# then words. This preserves semantic coherence better than a naive character split.

# ── EMBEDDINGS ────────────────────────────────────────────────────────────────
# An embedding model converts text → a dense vector (array of floats).
# Semantically similar text produces vectors that are geometrically close.
# "dog" and "puppy" will be near each other; "dog" and "invoice" will be far apart.
from langchain_openai import OpenAIEmbeddings
# OpenAI's text-embedding-3-small produces 1536-dimensional vectors.
# You can also use: HuggingFaceEmbeddings (free, local), CohereEmbeddings etc.

# ── VECTOR STORE ──────────────────────────────────────────────────────────────
# A vector store is a database optimized for similarity search.
# Given a query vector, it finds the k stored vectors with smallest cosine distance.
from langchain_chroma import Chroma
# Chroma: embedded, no-server, persists to disk. Great for development.
# In production, switch to: langchain_postgres.PGVector (PostgreSQL + pgvector extension)

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=os.getenv("AI_API_KEY"),
    base_url=os.getenv("AI_ENDPOINT")
)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,       # Maximum characters per chunk
    chunk_overlap=50,     # Overlap between consecutive chunks.
    # Overlap is crucial — without it, a sentence split across two chunks
    # loses context. With overlap, both chunks contain the boundary sentence.
    length_function=len,  # How to measure chunk size (character count here)
    separators=["\n\n", "\n", " ", ""],
    # Try splitting at paragraphs first, then lines, then words, then chars.
    # This ordering preserves the most semantic structure.
)

def load_document(file_path: str, file_type: str):
    """
    Load a document file and return LangChain Document objects.
    Each Document has:
      - page_content: the raw text of that page/chunk
      - metadata: source file, page number, etc.
    """
    print(f"load_document::: Loading Document {file_path} with file_type: {file_type}")
    loaders = {
        "pdf":  lambda: PyPDFLoader(file_path),
        "docx": lambda: Docx2txtLoader(file_path),
        "txt":  lambda: TextLoader(file_path),
        "md":   lambda: UnstructuredMarkdownLoader(file_path),
    }
    loader_fn = loaders.get(file_type)
    if not loader_fn:
        raise ValueError(f"Unsupported file type: {file_type}")

    loader = loader_fn()
    return loader.load()   # Returns List[Document]

def ingest_document(
    file_path: str,
    file_name: str,
    collection: str = "default",
    tags: str = ""
) -> dict:

    start_time = time.time()
    """
    Full ingestion pipeline: load → split → embed → store.
    Returns a summary of what was ingested.
    """
    # 1. Determine file type from extension
    print(f"ingest_document::: Ingesting {file_path} with collection: {collection}")
    file_ext = Path(file_name).suffix.lstrip(".").lower()

    # 2. Load the document into LangChain Document objects
    documents = load_document(file_path, file_ext)

    # 3. Add custom metadata to every document chunk
    # This metadata is stored alongside each vector and returned with search results.
    # Use it for: source attribution, filtering by document, date-based retrieval, etc.
    for doc in documents:
        doc.metadata.update({
            "source_file": file_name,
            "collection": collection,
            "tags": tags,
            # page number is already set by PyPDFLoader
        })
    print("Updated metadata for all documents with source_file, collection, and tags.")

    # 4. Split into chunks
    # split_documents handles the Document objects properly — it preserves metadata
    # and doesn't split a Document from one page into chunks that span two pages.
    chunks = splitter.split_documents(documents)

    # 5. Embed and store in ChromaDB
    # Chroma.from_documents() calls embeddings.embed_documents(texts) internally,
    # then stores (vector, text, metadata) tuples. It returns a retriever interface.
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=collection,    # Namespace for logical separation
        persist_directory="./chroma_db"  # Directory where Chroma saves to disk
    )

    print("Stored chunks in ChromaDB with collection name:", collection)

    end_time = time.time()

    total_time = end_time - start_time
    print(f"Ingestion completed in {total_time} seconds.")

    return {
        "file_name": file_name,
        "collection": collection,
        "total_pages": len(documents),
        "total_chunks": len(chunks),
        "message": f"Successfully ingested {len(chunks)} chunks from {file_name}"
    }