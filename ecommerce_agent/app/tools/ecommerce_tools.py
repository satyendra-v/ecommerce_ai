import os
from dotenv import load_dotenv
import requests
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from langchain.tools import tool

load_dotenv()

ecommerce_be_service = os.getenv("ECOMMERCE_BE_SERVICE")

@tool
def search_products(query: str, name: str = "", max_price: float = None) -> str:
    """
    Search the product catalog. Check this when a user asks about available products,
    or wants to find specific products by name, type, or price range.

    Args:
        query (str): Search term(product name, type, or keyword)
        name (str, optional): Product name to search for. Defaults to "".
        max_price (float, optional): Maximum price filter in USD. Defaults to None.

    Returns:
        str: Search results in JSON format contains list of products that matches the filter
    """

    print(f"query: {query}")
    print(f"name: {name}")
    print(f"max_price: {max_price}")

    params = {"query": query}
    if max_price:
        params["max_price"] = max_price
    if name:
        params["name"] = name

    response = requests.get(f"{ecommerce_be_service}/api/products", params=params)

    print(f"API URL: {response.url}")
    print(f"Response status: {response.status_code}")
    print(f"Response text: {response.text}")

    products = response.json()

    print(f"Parsed products: {products}")

    if not products:
      print("No products found matching your criteria.")
      return "No products found matching your criteria."

    print(f"Found {len(products)} products matching your criteria.")
    lines = ["Found {} products".format(len(products))]

    for p in products:
        lines.append(f"  - ID:{p['productId']} | {p['name']} | ${p['price']} | {p.get('sku', 'N/A')}")

    return "\n".join(lines)


class CalculatorInput(BaseModel):
    """Input for calculator."""

    expression: str = Field(description="Math expression to evaluate")

@tool(args_schema=CalculatorInput)
def calculator(expression: str) -> str:
    """Perform mathematical calculations."""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Error: {e}"



class SearchInput(BaseModel):
    """Input for search."""

    query: str = Field(description="Search query")

@tool(args_schema=SearchInput)
def search_information(query: str) -> str:
    """Search for factual information.Use this tool when user asked any information"""
    results = {
        "Capital of France" : "Paris",
        "Virat Kohli Centuries" : "85",
        "king of the cricket" : "Virat Kohli"
    }
    print("search_information invoked")
    return results.get(query.lower(), "No results found")

def get_tools() -> list[BaseTool]:
    return [search_products, search_information, calculator]

tools = {
    "calculator" : calculator,
    "search_products" : search_products,
    "search_information": search_information
}