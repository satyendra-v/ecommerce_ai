from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

import os
from dotenv import load_dotenv

load_dotenv()

ai_model = os.getenv("AI_MODEL")
ai_endpoint = os.getenv("AI_ENDPOINT")
ai_api_key = os.getenv("AI_API_KEY")

# -------- LLM --------
llm = ChatOpenAI(
    model=ai_model,
    base_url=ai_endpoint,
    api_key=ai_api_key,
    temperature=0
)

# -------- Text Splitter --------
# Why split? LLM context windows are limited. A 100-page PDF can't fit in a prompt. So, we split into chunks of ~500 tokens. Each chunk is stored as a separate vector.
# At query time we retrieve the most relevant chunks, not the whole document.
# It tries to split on paragraph breaks first (\n\n), then sentences (\n),then words. This preserves semantic coherence better than a naive character split.
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

# -------- Embeddings --------
# An embedding model converts text → a dense vector (array of floats).Semantically similar text produces vectors that are geometrically close.
# Ex:- "dog" and "puppy" will be near each other; "dog" and "invoice" will be far apart.
# OpenAI's text-embedding-3-small produces 1536-dimensional vectors.Can also use: HuggingFaceEmbeddings (free, local), CohereEmbeddings etc.

# A vector store is a database optimized for similarity search.
# Given a query vector, it finds the k stored vectors with smallest cosine distance.
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    base_url=ai_endpoint,
    api_key=ai_api_key
)