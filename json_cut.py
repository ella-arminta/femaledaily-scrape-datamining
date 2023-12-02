import json
import random

# Load JSON data from a file
with open('products_urls_asli.json', 'r') as json_file:
    data = json.load(json_file)

# Pick 300 random elements from the data
random_elements = random.sample(data, 300)

# Save the selected elements to another JSON file
with open('products_urls_edited.json', 'w') as output_file:
    json.dump(random_elements, output_file, indent=2)
