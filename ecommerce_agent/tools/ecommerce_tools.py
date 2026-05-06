import os
from dotenv import load_dotenv
import requests

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

    response = requests.get(f"{ecommerce_be_service}/products", params=params)

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
