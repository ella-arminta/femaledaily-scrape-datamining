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
        try :
            # product_brand
            product_brand = self.driver.find_element(By.CSS_SELECTOR,'.product-brand').text
            # product_name
            product_name = self.driver.find_element(By.CSS_SELECTOR, '.product-name').text
            # subcategory
            category = self.driver.find_element(By.CSS_SELECTOR, '.breadcrumb .breadcrumb-section-text:nth-child(2)').text
            # harga
            harga = self.driver.find_element(By.CSS_SELECTOR, '.product-price').text
            # rating
            rating = self.driver.find_element(By.CSS_SELECTOR, '.total p').text
            
        except Exception as e:
            print(e)
            pass
        
        return {
            'product_brand' : product_brand,
            'product_name' : product_name,
            'category' : category,
            'harga' : harga,
            'rating' : rating
        }

    def get_reviews(self):
        url = self.url
        url = url[:-1]

        umurDict = {}
        skinType1Dict = {}
        skinType2Dict = {}
        skinType3Dict = {}
        purchasePointDict = {}
        for i in range(1,3):
            self.driver.get(url + str(i))
            reviews = self.driver.find_elements(By.CSS_SELECTOR, '.review-card')
            for r in reviews:
                try:
                    # purchase poin (paling banyak dilihat dari review), 
                    purchase_point = r.find_element(By.CSS_SELECTOR, '.information-wrapper p:nth-child(2) b').text
                    if purchase_point in purchasePointDict:
                        purchasePointDict[purchase_point] += 1
                    else:
                        purchasePointDict[purchase_point] = 1
                    
                    # umur
                    umur = r.find_element(By.CSS_SELECTOR, '.profile-age').text
                    if umur in umurDict:
                        umurDict[umur] += 1
                    else:
                        umurDict[umur] = 1

                    # skin type(rekomendasi terbagus, diambil skin type e apa), 
                    element = r.find_element(By.CSS_SELECTOR, '.profile-description').text
                    skin_types = [word.strip() for word in element.split(',')]
                    print(skin_types)

                    skin_type1 = skin_types[0]
                    if skin_type1 in skinType1Dict:
                        skinType1Dict[skin_type1] += 1
                    else:
                        skinType1Dict[skin_type1] = 1

                    skin_type2 = skin_types[1]
                    if skin_type2 in skinType2Dict:
                        skinType2Dict[skin_type2] += 1
                    else:
                        skinType2Dict[skin_type2] = 1

                    skin_type3 = skin_types[2]
                    if skin_type3 in skinType3Dict:
                        skinType3Dict[skin_type3] += 1
                    else:
                        skinType3Dict[skin_type3] = 1

                except Exception as e:
                    print(e)
                    pass

        max_umur = max(umurDict, key=umurDict.get)
        max_skin1 = max(skinType1Dict, key=skinType1Dict.get)
        max_skin2 = max(skinType2Dict, key=skinType2Dict.get)
        max_skin3 = max(skinType3Dict, key=skinType3Dict.get)
        max_purchase_point = max(purchasePointDict, key=purchasePointDict.get)
        
        return {
            'umur' : max_umur,
            'skin1' : max_skin1,
            'skin2' : max_skin2,
            'skin3' : max_skin3,
            'purchase_point' : max_purchase_point
        }

    def scrape_data(self):
        # Add an explicit wait
        element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.product-brand')))

        product_info = self.get_product_info()
        reviews = self.get_reviews()

        # combine the two dictionaries 
        data = {**product_info, **reviews}

        return data

       

    def close_driver(self):
        self.driver.quit()

with open('products_urls_edited.json', 'r') as json_file:
    product_urls = json.load(json_file)

# product_urls = [
#     'https://reviews.femaledaily.com/products/moisturizer/face-mist/pixy/aqua-beauty-protecting-mist?cat=&cat_id=0&age_range=&skin_type=&skin_tone=&skin_undertone=&hair_texture=&hair_type=&order=high_rating&page=1',
#     'https://reviews.femaledaily.com/products/nails/nail-polish-remover/tokyo-night/nail-polish-remover-pink?cat=&cat_id=0&age_range=&skin_type=&skin_tone=&skin_undertone=&hair_texture=&hair_type=&order=high_rating&page=1'
# ]

df = pd.DataFrame()
for prod_url in product_urls:
    scraper = FemaleDailyScraper(prod_url)
    row = scraper.scrape_data()
    print(row)

    # Convert the data to a DataFrame
    dftemp = pd.DataFrame([row])

    df = df._append(dftemp, ignore_index=True)

    print(df)
    print('data appended to excel')

# Save the DataFrame to an Excel file, append mode
with pd.ExcelWriter('scrape_result.xlsx', engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
    # Write the DataFrame to the Excel file
    # df.to_excel(writer, sheet_name='Sheet1', index=True, header=not writer.sheets['Sheet1'])
    df.to_excel(writer, sheet_name='Sheet1', index=False, header=True)
