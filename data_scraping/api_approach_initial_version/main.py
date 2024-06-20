import json
import pandas as pd

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
df.to_csv('products.csv', index=False, encoding='utf-16')

print("Data has been successfully converted to CSV format in UTF-16 encoding.")
