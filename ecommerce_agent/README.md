# E-Commerce AI Agent

A sophisticated AI agent that uses **ReAct**, **Function Calling**, **RAG**, and **MCP** to provide intelligent e-commerce assistance by integrating with a Spring Boot backend service.

## Architecture

```
ecommerce_agent/
├── agent/
│   ├── __init__.py              # Agent module exports
│   └── agent.py                 # ReAct agent with LLM, tools, and RAG
├── tools/
│   ├── __init__.py
│   └── ecommerce_tools.py       # LangChain tools for Spring Boot API calls
├── prompts/
│   └── system_prompt.txt        # Agent system instructions
├── data/
│   ├── __init__.py
│   └── rag_setup.py             # Vector store creation script
├── integrations/
│   └── mcp_adapter.py           # MCP server integration (optional)
├── main.py                       # Entry point
├── requirements.txt              # Python dependencies
├── .env                          # Environment variables
└── README.md                     # This file
```

## Key Components

### 1. **ReAct Agent** (`agent/agent.py`)
- Uses `ChatOpenAI` with GPT-4 as the reasoning engine
- Implements the ReAct (Reasoning + Acting) loop
- Iteratively reasons and takes actions using tools

### 2. **Tools** (`tools/ecommerce_tools.py`)
- **search_products**: Search products via Spring Boot API
- **get_product_details**: Fetch detailed product information
- **add_to_cart**: Add items to user's cart
- Integrated as LangChain `@tool` decorators for function calling

### 3. **RAG (Retrieval-Augmented Generation)** (`data/rag_setup.py`)
- Vector store using FAISS and OpenAI embeddings
- Augments agent with product knowledge without API calls
- Similarity search for product recommendations

### 4. **Prompts** (`prompts/system_prompt.txt`)
- System instructions guiding agent behavior
- Customizable for different use cases

### 5. **MCP Integration** (`integrations/mcp_adapter.py` - Optional)
- Model Context Protocol for extensible AI interactions
- Allows integration of external services and protocols

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Edit `.env` file:
```env
OPENAI_API_KEY=sk-your-api-key
SPRING_BOOT_URL=http://localhost:8080
```

### 3. Create RAG Vector Store
```bash
python data/rag_setup.py
```

This creates a FAISS vector store with sample product data at `data/vectorstore/`.

### 4. Start Spring Boot Service
Ensure your Spring Boot e-commerce service is running on `http://localhost:8080` with these endpoints:
- `GET /products/search?q=<query>` - Search products
- `GET /products/{id}` - Get product details
- `POST /cart/add` - Add to cart

### 5. Run the Agent
```bash
python main.py
```

Example interactions:
```
Enter your query: What wireless headphones do you recommend under $300?
```

## How It Works

1. **User Query** → Agent receives natural language request
2. **Reasoning** → ReAct agent thinks about which tools to use
3. **Tool Selection** → Agent chooses from: RAG Search, Product Search, Product Details, Add to Cart
4. **Execution** → Tools make API calls to Spring Boot or search vector store
5. **Response** → Agent combines results and provides natural language answer

## Function Calling Flow

```
LLM (ChatOpenAI) decides which tool to use
    ↓
Tool is invoked with parameters
    ↓
Tool returns data (API response or RAG results)
    ↓
LLM processes response and decides next action
    ↓
Final response to user or trigger another tool
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key for ChatOpenAI and embeddings |
| `SPRING_BOOT_URL` | Yes | Base URL of Spring Boot service |
| `AI_API_KEY` | No | Alternative API key for Azure AI (optional) |
| `AI_ENDPOINT` | No | Azure AI endpoint (optional) |

## Dependencies

Key packages in `requirements.txt`:
- **langchain**: Core AI framework
- **langchain-openai**: OpenAI LLM integration
- **langchain-community**: FAISS and other community tools
- **faiss-cpu**: Vector database
- **python-dotenv**: Environment management

## Extending the Agent

### Add a New Tool
```python
from langchain.tools import tool

@tool
def my_custom_tool(param: str) -> str:
    """Tool description for the agent."""
    # Your implementation
    return result
```

Add it to `tools` list in `agent/agent.py`.

### Customize System Prompt
Edit `prompts/system_prompt.txt` to change agent behavior and instructions.

### Integrate MCP Server
Use `integrations/mcp_adapter.py` to add Model Context Protocol support for pluggable services.

## Testing

Run unit tests:
```bash
python -m pytest tests/
```

## Troubleshooting

**ImportError: No module named 'langchain'**
```bash
pip install --upgrade langchain langchain-openai langchain-community
```

**APIError: Incorrect API key**
- Ensure `OPENAI_API_KEY` is set correctly in `.env`

**Connection refused to Spring Boot**
- Verify Spring Boot is running on `http://localhost:8080`
- Check `SPRING_BOOT_URL` in `.env`

**RAG vector store not found**
```bash
python data/rag_setup.py
```

## Future Enhancements

- [ ] Memory management (conversation history)
- [ ] Multi-turn conversation support
- [ ] Custom embedding model fine-tuning
- [ ] Async tool execution for parallel API calls
- [ ] Streaming responses
- [ ] Production deployment (FastAPI/Flask wrapper)
- [ ] MCP server fully integrated
- [ ] Monitoring and logging

---

**Last Updated**: May 2026

