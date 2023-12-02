from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import json

with open('category_urls.json', 'r') as json_file:
    category_urls = json.load(json_file)

driver = webdriver.Chrome()
subcat_list =[]
for cat_url in category_urls : 
    driver.get(cat_url)
    subcats = driver.find_elements(By.CSS_SELECTOR, '.category-landing-list .category-landing-column  a')
    for subcat in subcats: 
        subcat_href = subcat.get_attribute('href')[:-1]
        subcat_list.append(subcat_href)
    print('subcat_list : ', subcat_list)
    print('checkpoin')

with open("subcat_urls.json", "w") as json_file:
    json.dump(subcat_list, json_file, indent=2)

# product_list = []
# for i in range(1,4):
#     subcat_page = subcat_list[0] + str(i)
#     driver.get(subcat_page)
#     products = driver.find_elements(By.CSS_SELECTOR,'.product-item .product-card-catalog a')
#     for product in products:
#         product_list.append(product.get_attribute('href'))

# print('product_list : ', product_list)

    
# data = {
#     'username' : username,
#     'reviews' : review_list,
# }
# json_string = json.dumps(data, indent=2) 
# print(json_string)

# with open("products_urls.json", "w") as json_file:
#     json.dump(product_list, json_file, indent=2)

# df = pd.DataFrame(data)
# print('done')
# # Save DataFrame to CSV file
# df.to_excel('female_daily.xlsx', index=True)

# Add an explicit wait
wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.category-landing-list')))

# pip install openpyxl