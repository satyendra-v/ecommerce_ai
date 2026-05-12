from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from langchain_community.chat_message_histories import ChatMessageHistory

from model import llm
from state import AgentState
import os
from dotenv import load_dotenv

load_dotenv()

# With RAG


# ── VECTOR STORE ──────────────────────────────────────────────────────────────
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=os.getenv("AI_API_KEY"),
    base_url=os.getenv("AI_ENDPOINT")
)

# 1. Load the vector store for this collection (or create it if it doesn't exist)
vectorstore = Chroma(
    collection_name="company-docs",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

# 2. Create a retriever from the vector store.
retriever = vectorstore.as_retriever(
    # MMR(Maximal Marginal Relevance) is a search strategy that balances relevance and diversity in the search results.
    # MMR ensures retrieved chunks cover different aspects.
    # It helps to retrieve results that are not only relevant to the query but also diverse from each other, which can be particularly useful in scenarios like knowledge retrieval where you want a variety of information.
    search_type="mmr",
    search_kwargs={"k": 3, "fetch_k": 9} # Fetching 3x more to apply MMR re-ranking
)

# ── SUPPORT AGENT PROMPT ──────────────────────────────────────────────────────
SUPPORT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a friendly customer support agent for an e-commerce company.
Answer questions using the retrieved knowledge base context below.
If the answer isn't in the context, say so honestly — don't make things up.
If the customer has an issue requiring a refund or ticket, let them know the operations agent will handle it.

Knowledge Base Context:
{context}
"""),
    MessagesPlaceholder(variable_name="history"),  # Injects conversation history
    ("human", "{question}"),
])

# Per-session memory store
session_memories: dict[str, ChatMessageHistory] = {}
def get_session_memory(session_id: str) -> ChatMessageHistory:
    if session_id not in session_memories:
        session_memories[session_id] = ChatMessageHistory()
    return session_memories[session_id]


def support_node(state: AgentState) -> dict:
    """
    Support agent: retrieves relevant KB articles and answers the user's question.
    Maintains per-session conversation memory.
    """
    print("Support agent: retrieves relevant KB articles and answers the user's question.")
    # Extract the latest human message from state
    latest_message = next(
        (m.content for m in reversed(state["messages"])
         if isinstance(m, HumanMessage)),
        ""
    )

    # 1. Retrieve relevant knowledge base chunks
    docs = retriever.invoke(latest_message)
    context = "\n\n---\n\n".join(
        f"[Source: {d.metadata.get('source', 'KB')}]\n{d.page_content}"
        for d in docs
    )

    # 2. Build chain with memory
    chain = SUPPORT_PROMPT | llm | StrOutputParser()
    chain_with_memory = RunnableWithMessageHistory(
        chain,
        get_session_memory,
        input_messages_key="question",
        history_messages_key="history",
    )

    # 3. Generate response using both context and conversation history
    answer = chain_with_memory.invoke(
        {"question": latest_message, "context": context},
        config={"configurable": {"session_id": state["session_id"]}}
    )

    print(f"Support agent: answer: {answer[:20]}")

    return {
        "messages": [AIMessage(content=answer, name="support_agent")],
        "action_log": [{"node": "support", "kb_chunks_used": len(docs)}],
    }

def test_support_node(state: AgentState) :
    print("INVOKED SUPPORT NODE")