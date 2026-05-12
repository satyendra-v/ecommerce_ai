from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import os
from model import llm
import time

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=os.getenv("AI_API_KEY"),
    base_url=os.getenv("AI_ENDPOINT")
)

# ── RAG PROMPT ────────────────────────────────────────────────────────────────
# This prompt is the core of RAG. It provides retrieved context to the model
# and instructs it to answer ONLY from that context, not from its training data.
# This prevents hallucination — the model cites actual document content.
RAG_PROMPT = ChatPromptTemplate.from_template("""
You are an assistant that answers questions based ONLY on the provided context.
If the answer is not in the context, say "I don't have information about that in the documents."
Do NOT make up information. Always cite which document your answer comes from.

Context from documents:
{context}

Question: {question}

Answer (with source citations):
""")

def format_docs_with_sources(docs) -> str:
    """
    Formats retrieved document chunks into a single context string.
    Includes source file name and page number for citation.
    Each chunk is labeled so the LLM can reference which document it came from.
    """
    formatted = []
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get("source_file", "Unknown")
        page = doc.metadata.get("page", "?")
        # Format: [1] Source: filename.pdf, Page 3
        formatted.append(
            f"[{i}] Source: {source}, Page {page}\n{doc.page_content}"
        )
    print("format_docs_with_sources :: Formatted documents with sources:")
    return "\n\n---\n\n".join(formatted)

def query_rag(
    question: str,
    collection: str = "default",
    top_k: int = 4,
    cite_sources: bool = True
) -> dict:

    start_time = time.time()
    """
    Full RAG query pipeline: embed question → retrieve → generate answer.
    """
    print(f"query_rag:: Querying {collection} with question: {question}")

    # 1. Load the vector store for this collection
    vectorstore = Chroma(
        collection_name=collection,
        embedding_function=embeddings,
        persist_directory="./chroma_db"
    )
    print("query_rag :: Loaded vector store with collection:", collection)

    # 2. Create a retriever from the vector store.
    # The retriever's .invoke(query) method:
    #   a. Embeds the query text into a vector
    #   b. Performs cosine similarity search
    #   c. Returns the top_k most similar document chunks
    retriever = vectorstore.as_retriever(
        search_type="mmr",  # MMR = Maximal Marginal Relevance
        # MMR balances relevance AND diversity. Without it, you might get 4 chunks
        # from the same paragraph. MMR ensures retrieved chunks cover different aspects.
        search_kwargs={
            "k": top_k,          # Number of chunks to return
            "fetch_k": top_k * 3 # Fetch 3x more candidates, then apply MMR re-ranking
        }
    )

    # 3. Retrieve relevant chunks (for returning to the user)
    retrieved_docs = retriever.invoke(question)

    print(f"query_rag :: Retrieved {len(retrieved_docs)} documents")

    # 4. Build the RAG chain using LCEL
    # RunnablePassthrough passes the question through to the prompt unchanged.
    # The retriever is called with the question, formats the results, and inserts as context.
    rag_chain = (
        {
            "context": retriever | format_docs_with_sources,
            "question": RunnablePassthrough()
        }
        | RAG_PROMPT
        | llm
        | StrOutputParser()
    )

    # 5. Generate the answer
    answer = rag_chain.invoke(question)

    print(f"query_rag :: Generated answer......")


    # 6. Build response with source metadata
    sources = []
    if cite_sources:
        for doc in retrieved_docs:
            sources.append({
                "file": doc.metadata.get("source_file", "unknown"),
                "page": doc.metadata.get("page", None),
                "snippet": doc.page_content[:200] + "..."
            })
    end_time = time.time()
    total_time = "{:.3f}".format(end_time - start_time)
    print(f"query_rag :: Retrieved in {total_time} seconds")

    return {
        "question": question,
        "answer": answer,
        "sources": sources,
        "chunks_retrieved": len(retrieved_docs)
    }