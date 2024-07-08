import httpx
import asyncio

# Replace with your Shopify API credentials and store information
SHOPIFY_API_KEY = 'your_api_key'
SHOPIFY_PASSWORD = 'your_api_password'
SHOP_NAME = 'your_shop_name'

# Base URL for the Shopify API
BASE_URL = f'https://{SHOPIFY_API_KEY}:{SHOPIFY_PASSWORD}@{SHOP_NAME}.myshopify.com/admin/api/2021-07'

# Fetch a page of products from Shopify API
async def fetch_products(session, page_info = None):
    url = f"{BASE_URL}/products.json"
    params = {
        "limit": 250,
    }
    if page_info:
        params["page_info"] = page_info

    try:
        response = await session.get(url, params = params)
        response.raise_for_status()  # handle HTTP response
        data = response.json()
        return data["products"], data.get("link", {}).get("next") # link to next page    
    except httpx.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return [], None  # Return empty list and None for page_info to stop fetching    
    except Exception as err:
        print(f"Other error occurred: {err}")
        return [], None  # Return empty list and None for page_info to stop fetching

# Filter products by their variants
async def filter_products(products, filter_value, option_key = "Option1"):
    filtered = []
    for product in products:
        for variant in product["variants"]:
            if variant[option_key] == filter_value:
                filtered.append(product)
                break
    return filtered

# Fetch all products
async def fetch_all_products():
    async with httpx.AsyncClient() as session:
        all_products = []
        page_info = None
        while True:
            products, page_info = await fetch_products(session, page_info)
            if not products:  # If no products fetched, stop fetching
                break
            all_products.extend(products)
            if not page_info:
                break
        return all_products

async def main():
    try:
        # Fetch all products
        all_products = await fetch_all_products()

        # Filter products with Option1='Green'
        green_products = await filter_products(all_products, "Green")

        # Print the filtered products
        for product in green_products:
            print(f"Product ID: {product['id']}, Title: {product['title']}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__": # For terminal execution
    asyncio.run(main())
