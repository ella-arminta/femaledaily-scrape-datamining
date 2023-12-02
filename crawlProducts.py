from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import json

with open('subcat_urls.json', 'r') as json_file:
    subcat_urls = json.load(json_file)

driver = webdriver.Chrome()

product_list = []
for subcat_url in subcat_urls :
    for i in range(1,4):
        subcat_page = subcat_url + str(i)
        driver.get(subcat_page)
        products = driver.find_elements(By.CSS_SELECTOR,'.product-item .product-card-catalog a')
        for product in products:
            product_list.append(product.get_attribute('href'))

print('product_list : ', product_list)

with open("products_urls.json", "w") as json_file:
    json.dump(product_list, json_file, indent=2)
    
# data = {
#     'username' : username,
#     'reviews' : review_list,
# }
# json_string = json.dumps(data, indent=2) 
# print(json_string)


# df = pd.DataFrame(data)
# print('done')
# # Save DataFrame to CSV file
# df.to_excel('female_daily.xlsx', index=True)

# Add an explicit wait
wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.product-item')))

# pip install openpyxl