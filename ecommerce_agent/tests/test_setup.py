import os
import sys
from dotenv import load_dotenv

from app.utils.model import llm

def test_llm() -> dict[str, str]:

    llm_response = {}
    print("Testing AI provider connection...\n")
    load_dotenv()

    ai_model = os.getenv("AI_MODEL")
    ai_endpoint = os.getenv("AI_ENDPOINT")
    ai_api_key = os.getenv("AI_API_KEY")


    if not ai_api_key or not ai_endpoint:
        print(" ERROR : Missing AI_API_KEY/ AI_ENDPOINT in .env file")
        sys.exit(1)

    try:
        model = llm
        response = model.invoke("Say 'Setup successful!'")

        print(f"Model response: {response.content}")
        print(f"Model : {ai_model}")
        print(f"Endpoint : {ai_endpoint}")
        print("Setup successful!")

        llm_response["Model Response"] = response.content
        llm_response["Model"] = ai_model
        llm_response["Endpoint"] = ai_endpoint

    except Exception as error:
        print(f" ERROR : {str(error)}")
    return llm_response


if __name__ == "__main__" :
    test_llm()