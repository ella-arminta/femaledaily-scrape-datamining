import json
import random

# Load JSON data from a file
with open('products_urls_asli.json', 'r') as json_file:
    data = json.load(json_file)

# with open('products_urls_edited1.json', 'r') as json_file: #step 2
#     data2 = json.load(json_file)

# Filter the data to exclude rows with product_brand starting with the specified URL
filtered_data = [row for row in data if not row.startswith("https://reviews.femaledaily.com/brands/")] #step 1
# filtered_data = [row for row in data if not row.startswith("https://reviews.femaledaily.com/brands/") and row not in data2] #step 2


# Pick 300 random elements from the filtered data
# random_elements = random.sample(filtered_data, min(300, len(filtered_data))) #step 1
# random_elements = random.sample(filtered_data, min(46, len(filtered_data))) #step 2
random_elements = random.sample(filtered_data, min(365, len(filtered_data))) #step 3 with category scrape


# Save the selected elements to another JSON file
# with open('products_urls_edited.json', 'w') as output_file: #step1
#     json.dump(random_elements, output_file, indent=2)

# with open('products_urls_edited2.json', 'w') as output_file: #step2
#     json.dump(random_elements, output_file, indent=2)

with open('products_urls_fix.json', 'w') as output_file: #step2
    json.dump(random_elements, output_file, indent=2)
