import json
import random

# Load JSON data from a file
with open('products_urls_asli.json', 'r') as json_file:
    data = json.load(json_file)

# Filter the data to exclude rows with product_brand starting with the specified URL
filtered_data = [row for row in data if not row.startswith("https://reviews.femaledaily.com/brands/")]

# Pick 300 random elements from the filtered data
random_elements = random.sample(filtered_data, min(300, len(filtered_data)))

# Save the selected elements to another JSON file
with open('products_urls_edited.json', 'w') as output_file:
    json.dump(random_elements, output_file, indent=2)
