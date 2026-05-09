from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

ai_model = os.getenv("AI_MODEL")
ai_endpoint = os.getenv("AI_ENDPOINT")
ai_api_key = os.getenv("AI_API_KEY")

llm = ChatOpenAI(
            model=ai_model,
            base_url=ai_endpoint,
            api_key=ai_api_key,
            temperature=0
        )