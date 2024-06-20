import requests
from pyquery import PyQuery as pq
import json
import time
import pandas as pd

base_url = 'https://parts.cat.com/api/product/list?sortBy=2&urlKeyword=shop-by-attachment&storeIdentifier=CATCorp&locale=en_US&storeId=21801&langId=-1'
target_url = 'https://parts.cat.com/en/catcorp/shop-by-attachment'

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,de;q=0.6',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
    'Referer': 'https://parts.cat.com/en/catcorp/shop-by-attachment?beginIndex=32&pageSize=16&productBeginIndex=32',
    'Sec-Ch-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}

def fetch_initial_details():
    try:
        response = requests.get(target_url, headers=headers)
        cookies = response.cookies.get_dict()
        doc = pq(response.content)

        tracking_id = doc('meta[name="X-Cat-Api-Tracking-Id"]').attr('content')
        pcc_session_id = doc('meta[name="X-Cat-Pcc-Session-Id"]').attr('content')

        return cookies, tracking_id, pcc_session_id
    except Exception as e:
        print('Error fetching initial details:', str(e))
        raise

def fetch_products(offset, cookies, tracking_id, pcc_session_id):
    url = f"{base_url}&offset={offset}"
    try:
        response = requests.get(url, headers={**headers, 'Cookie': "; ".join([f"{k}={v}" for k, v in cookies.items()]), 'X-Cat-Api-Tracking-Id': tracking_id, 'X-Cat-Pcc-Session-Id': pcc_session_id})
        return response.json().get('products', [])
    except Exception as e:
        print(f"Error fetching data from offset {offset}:", str(e))
        raise

def delay(s):
    time.sleep(s)

def main():
    all_products = []
    cookies, tracking_id, pcc_session_id = fetch_initial_details()

    for offset in range(0, 79):
        success = False
        attempts = 0
        while not success and attempts < 5:
            try:
                print(f"Fetching data for offset {offset}, attempt {attempts + 1}")
                products = fetch_products(offset, cookies, tracking_id, pcc_session_id)
                all_products.extend(products)
                success = True
            except Exception:
                attempts += 1
                if attempts < 5:
                    print("Retrying after error...")
                    delay(2)
                else:
                    print(f"Failed to fetch data for offset {offset} after {attempts} attempts")
        delay(0.5)

    with open('products.json', 'w') as f:
        json.dump(all_products, f, indent=2)
    print('Data saved to products.json')

    print("Started converting JSON to CSV")

    # Load the JSON data
    with open('products.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Extract needed properties
    products_list = []
    for product in data:
        product_info = {
            "longDescription": product.get("longDescription", ""),
            "shortDescription": product.get("shortDescription", ""),
            "parentPartNumber": product.get("parentPartNumber", ""),
            "name": product.get("name", ""),
            "partNumber": product.get("partNumber", ""),
            "manufacturer": product.get("manufacturer", ""),
            "type": product.get("type", ""),
            "thumbnail": product.get("thumbnail", ""),
            "productURL": product.get("productURL", ""),
            "imageURL": product.get("imageURL", ""),
            "buyable": product.get("buyable", False),
        }

        # Flatten attributes
        for attribute in product.get("attributes", []):
            attr_name = f"{attribute['name']}_{attribute['uom']}"
            product_info[attr_name] = attribute.get("value", "")

        products_list.append(product_info)

    # Convert to DataFrame
    df = pd.DataFrame(products_list)

    # Save DataFrame to CSV in UTF-16 encoding
    df.to_csv('products.csv', index=False, encoding='utf-8')

    print("Data has been successfully converted to CSV format")

if __name__ == '__main__':
    main()
