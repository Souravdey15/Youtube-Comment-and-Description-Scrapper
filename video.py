from selenium import webdriver 
import pandas as pd 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

video_id_files= open("video_id.txt")
links = []
for i in video_id_files.readline():
    links.append(i)

print(len(links))
df = pd.DataFrame(columns = ['link', 'title', 'description', 'category'])
wait = WebDriverWait(driver, 10)
v_category = "CATEGORY_NAME"
for x in links:
            driver = webdriver.Chrome()
            driver.get("C:\\Study\\Research Paper\\chromedriver_win32\\chromedriver.exe")
            user_data = driver.find_elements_by_xpath('//*[@id="video-title"]')
            driver.get(x)
            v_id = x.strip('https://www.youtube.com/watch?v=')
            v_title = wait.until(EC.presence_of_element_located(
                           (By.CSS_SELECTOR,"h1.title yt-formatted-string"))).text
            v_description =  wait.until(EC.presence_of_element_located(
                                         (By.CSS_SELECTOR,"div#description yt-formatted-string"))).text
            df.loc[len(df)] = [v_id, v_title, v_description, v_category]
frames = [df_travel, df_science, df_food, df_manufacturing, df_history, df_artndance]
df_copy = pd.concat(frames, axis=0, join='outer', join_axes=None, ignore_index=True,
                            keys=None, levels=None, names=None, verify_integrity=False, copy=True)