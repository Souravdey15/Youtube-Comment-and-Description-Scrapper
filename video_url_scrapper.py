# scrape-youtube-channel-videos-url.py
#_*_coding: utf-8_*_

import sys, time, datetime,os
from selenium import webdriver

import time
start_time = time.time()

inURLs, usaURLs= [
					"https://www.youtube.com/user/KFCinIndia/videos",
					"https://www.youtube.com/user/McDIndiaOfficial/videos",
					"https://www.youtube.com/c/DominosPizzaIndia/videos",
					"https://www.youtube.com/c/PizzaHutIN/videos"
				], [
					"https://www.youtube.com/c/kfc/videos",
					"https://www.youtube.com/c/McDonalds/videos",
					"https://www.youtube.com/c/dominos/videos",
					"https://www.youtube.com/user/pizzahut/videos"
]

for url in inURLs:
	channelid = url.split('/')[4]
	driver = webdriver.Chrome('C:\\Study\\Research Paper\\chromedriver_win32\\chromedriver.exe')
	driver.get(url)
	time.sleep(5)
	dt=datetime.datetime.now().strftime("%Y%m%d%H%M")
	height = driver.execute_script("return document.documentElement.scrollHeight")
	lastheight = 0

	while True:
		if lastheight == height:
			break
		lastheight = height
		driver.execute_script("window.scrollTo(0, " + str(height) + ");")
		time.sleep(2)
		height = driver.execute_script("return document.documentElement.scrollHeight")

	if(not os.path.exists("India")):
		os.mkdir("India")


	user_data = driver.find_elements_by_xpath('//*[@id="video-title"]')
	for i in user_data:
		link = (i.get_attribute('href'))
		videoID=link[link.index('='):]
		f = open("India\\"+channelid+'-'+dt+'.txt', 'a+')
		f.write(videoID + '\n')
	f.close
	driver.quit()

for url in usaURLs:
	channelid = url.split('/')[4]
	driver = webdriver.Chrome('C:\\Study\\Research Paper\\chromedriver_win32\\chromedriver.exe')
	driver.get(url)
	time.sleep(5)
	dt = datetime.datetime.now().strftime("%Y%m%d%H%M")
	height = driver.execute_script("return document.documentElement.scrollHeight")
	lastheight = 0

	while True:
		if lastheight == height:
			break
		lastheight = height
		driver.execute_script("window.scrollTo(0, " + str(height) + ");")
		time.sleep(2)
		height = driver.execute_script("return document.documentElement.scrollHeight")

	if (not os.path.exists("USA")):
		os.mkdir("USA")

	user_data = driver.find_elements_by_xpath('//*[@id="video-title"]')
	for i in user_data:
		link = (i.get_attribute('href'))
		videoID = link[link.index('='):]
		f = open("USA\\" + channelid + '-' + dt + '.txt', 'a+')
		f.write(videoID + '\n')
	f.close
	driver.quit()

print("--- %s seconds ---" % (time.time() - start_time))