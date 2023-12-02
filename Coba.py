from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#D:\Downloads\edgedriver_win64\msedgedriver.exe
driver = webdriver.Edge()

url = 'https://www.youtube.com/@JohnWatsonRooney/videos'

driver.get(url)

# class="style-scope ytd-rich-item-renderer"
# #title
# //*[@id="video-title-link"]
# #views
# //*[@id="metadata-line"]/span[1]
# #day
# //*[@id="metadata-line"]/span[2]

# # Find an element by class name
# element = driver.find_element_by_class_name('style-scope ytd-rich-item-renderer')

# Now, find multiple elements under the located element
videos = driver.find_elements(By.CLASS_NAME,'style-scope ytd-rich-item-renderer')

for video in videos :
    title = video.find_element(By.XPATH,'.//*[@id="video-title-link"]').text
    views = video.find_element(By.XPATH,'.//*[@id="metadata-line"]/span[1]').text
    when = video.find_element(By.XPATH,'.//*[@id="metadata-line"]/span[2]').text
    print(title,views,when)

# Add an explicit wait
wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.XPATH, "//some/xpath")))

