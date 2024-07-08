import httpx
import asyncio

# Replace with your Shopify API credentials and store information
SHOPIFY_API_KEY = 'your_api_key'
SHOPIFY_PASSWORD = 'your_api_password'
SHOP_NAME = 'your_shop_name'

# Base URL for the Shopify API
BASE_URL = f'https://{SHOPIFY_API_KEY}:{SHOPIFY_PASSWORD}@{SHOP_NAME}.myshopify.com/admin/api/2021-07'

async def fetch_products(session, page_info=None):
    # Fetch a page of products from Shopify API
    url = f"{BASE_URL}/products.json"
    params = {
        "limit": 250,
    }
    if page_info:
        params["page_info"] = page_info

    response = await session.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data["products"], data.get("link", {}).get("next")

async def filter_products(products):
    # Filter products with Option1='Green' in their variants
    filtered = []
    for product in products:
        for variant in product["variants"]:
            if variant["option1"] == "Green":
                filtered.append(product)
                break
    return filtered

async def fetch_all_products():
    async with httpx.AsyncClient() as session:
        all_products = []
        page_info = None
        while True:
            products, page_info = await fetch_products(session, page_info)
            all_products.extend(products)
            if not page_info:
                break
        return all_products

async def main():
    # Fetch all products
    all_products = await fetch_all_products()

    # Filter products with Option1='Green'
    green_products = await filter_products(all_products)

    # Print the filtered products
    for product in green_products:
        print(f"Product ID: {product['id']}, Title: {product['title']}")

if __name__ == "__main__":
    asyncio.run(main())
