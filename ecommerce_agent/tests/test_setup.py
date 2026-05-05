import os
import sys

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

def test_setup():

    print("Testing AI provider connection...\n")
    load_dotenv()

    ai_model = os.getenv("AI_MODEL")
    ai_endpoint = os.getenv("AI_ENDPOINT")
    ai_api_key = os.getenv("AI_API_KEY")


    if not ai_api_key or not ai_endpoint:
        print(" ERROR : Missing AI_API_KEY/ AI_ENDPOINT in .env file")
        sys.exit(1)

    try:
        model = ChatOpenAI(
            model=ai_model,
            base_url=ai_endpoint,
            api_key=ai_api_key,
        )
        response = model.invoke("Say 'Setup successful!'")

        print(f"Model response: {response.content}")
        print(f"Model : {ai_model}")
        print(f"Endpoint : {ai_endpoint}")
        print("Setup successful!")
    except Exception as error:
        print(f" ERROR : {str(error)}")


if __name__ == "__main__" :
    test_setup()