from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import json

# url = 'https://account.femaledaily.com/user/fd/vlittacw?tab=reviews'

# driver = webdriver.Chrome()
# driver.get(url)

# # Use By.CSS_SELECTOR to find elements by compound class name

# username = driver.find_element(By.CSS_SELECTOR, '.profile-name-wrapper h4').text
# reviews = driver.find_elements(By.CSS_SELECTOR, '.profile-component-review-card')

# review_list = []

# for r in reviews:
#     try :
#         product_brand = r.find_element(By.CSS_SELECTOR, '.product__brand').text
#         product_name = r.find_element(By.CSS_SELECTOR, '.product__name').text
#         usage_period = r.find_element(By.CSS_SELECTOR, '.purchase-point:nth-child(1) span:nth-child(3)').text
#         purchase_point = r.find_element(By.CSS_SELECTOR, '.purchase-point:nth-child(2) span:nth-child(3)').text
#         the_review = r.find_element(By.CSS_SELECTOR, '.review-wrapper p').text
#         review_item = {
#             'product_brand' :product_brand,
#             'product_name' : product_name ,
#             'usage_period' :usage_period ,
#             'purchase_point' : purchase_point, 
#             'reviews' : the_review,
#         }

#         review_list.append(review_item)
#     except Exception as e:
#         print(e)
#         pass

# data = {
#     'username' : username,
#     'reviews' : review_list,
# }
# json_string = json.dumps(data, indent=2) 
# print(json_string)

# with open("data.json", "w") as json_file:
#     json.dump(data, json_file, indent=2)

# df = pd.DataFrame(data)
# print('done')
# # Save DataFrame to CSV file
# df.to_excel('female_daily.xlsx', index=True)

# # Add an explicit wait
# wait = WebDriverWait(driver, 20)
# element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.profile-name-wrapper h4')))

# pip install openpyxl

class FemaleDailyScraper:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        self.wait = WebDriverWait(self.driver, 20)

    def get_product_info(self):
        # category produk,
        category = self.driver.find_element(By.CSS_SELECTOR, '.breadcrumb .breadcrumb-section-text:nth-child(2)').text
        # range harga, 
        harga = self.driver.find_element(By.CSS_SELECTOR, '.product-price').text
        # umur
        umur = self.get_avg_umur_reviewer()
        # skin type(rekomendasi terbagus, diambil skin type e apa), 
        # purchase poin (paling banyak dilihat dari review), 
        # rating

        username = self.driver.find_element(By.CSS_SELECTOR, '.profile-name-wrapper h4').text
        return username

    def get_reviews(self):
        reviews = self.driver.find_elements(By.CSS_SELECTOR, '.profile-component-review-card')
        review_list = []

        for r in reviews:
            try:
                product_brand = r.find_element(By.CSS_SELECTOR, '.product__brand').text
                product_name = r.find_element(By.CSS_SELECTOR, '.product__name').text
                usage_period = r.find_element(By.CSS_SELECTOR, '.purchase-point:nth-child(1) span:nth-child(3)').text
                purchase_point = r.find_element(By.CSS_SELECTOR, '.purchase-point:nth-child(2) span:nth-child(3)').text
                the_review = r.find_element(By.CSS_SELECTOR, '.review-wrapper p').text

                review_item = {
                    'product_brand': product_brand,
                    'product_name': product_name,
                    'usage_period': usage_period,
                    'purchase_point': purchase_point,
                    'reviews': the_review,
                }

                review_list.append(review_item)
            except Exception as e:
                print(e)
                pass

        return review_list

    def get_avg_umur_reviewer(self):
        # https://reviews.femaledaily.com/products/moisturizer/face-mist/pixy/aqua-beauty-protecting-mist?cat=&cat_id=0&age_range=&skin_type=&skin_tone=&skin_undertone=&hair_texture=&hair_type=&order=high_rating&page=1
        reviews = self.driver.find_elements(By.CSS_SELECTOR, '.profile-component-review-card')
        review_list = []

        for r in reviews:
            try:
                product_brand = r.find_element(By.CSS_SELECTOR, '.product__brand').text
                product_name = r.find_element(By.CSS_SELECTOR, '.product__name').text
                usage_period = r.find_element(By.CSS_SELECTOR, '.purchase-point:nth-child(1) span:nth-child(3)').text
                purchase_point = r.find_element(By.CSS_SELECTOR, '.purchase-point:nth-child(2) span:nth-child(3)').text
                the_review = r.find_element(By.CSS_SELECTOR, '.review-wrapper p').text

                review_item = {
                    'product_brand': product_brand,
                    'product_name': product_name,
                    'usage_period': usage_period,
                    'purchase_point': purchase_point,
                    'reviews': the_review,
                }

                review_list.append(review_item)
            except Exception as e:
                print(e)
                pass

        return review_list

    def scrape_data(self):
        # Add an explicit wait
        element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.profile-name-wrapper h4')))

        username = self.get_user_info()
        reviews = self.get_reviews()

        data = {
            'username': username,
            'reviews': reviews,
        }

        json_string = json.dumps(data, indent=2)
        print(json_string)

        with open("data.json", "w") as json_file:
            json.dump(data, json_file, indent=2)

        df = pd.DataFrame(data)
        print('done')
        # Save DataFrame to Excel file
        df.to_excel('female_daily.xlsx', index=True)

    def close_driver(self):
        self.driver.quit()

with open('products_urls.json', 'r') as json_file:
    product_urls = json.load(json_file)

for prod_url in product_urls:
    scraper = FemaleDailyScraper(prod_url)
    scraper.scrape_data()