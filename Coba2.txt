from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

url = 'https://www.youtube.com/@JohnWatsonRooney/videos'

driver = webdriver.Chrome()
driver.get(url)



# Use By.CSS_SELECTOR to find elements by compound class name
videos = driver.find_elements(By.CSS_SELECTOR, '.style-scope.ytd-rich-item-renderer')

video_list = []

for video in videos:
    title = video.find_element(By.XPATH, './/*[@id="video-title-link"]').text
    views = video.find_element(By.XPATH, './/*[@id="metadata-line"]/span[1]').text
    when = video.find_element(By.XPATH, './/*[@id="metadata-line"]/span[2]').text
    vid_item = {
        'title': title,
        'views': views,
        'posted': when
    }

    video_list.append(vid_item)

df = pd.DataFrame(video_list)
print(df)

# Save DataFrame to CSV file
df.to_excel('youtube_videos.xlsx', index=False)



# Add an explicit wait
wait = WebDriverWait(driver, 20)
# element = wait.until(EC.presence_of_element_located((By.XPATH, "//some/xpath")))
element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='inner-header-container']")))