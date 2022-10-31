from selenium import webdriver
import urllib
import requests
import subprocess
from optparse import OptionParser
import sys
import json
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


'''
I prefer use to firefox for searching photos.
But you can use to chrome for searching photos.
'''


class Main:
	''' CONST VARIABLES'''
	SCROLL_PAUSE_TIME = 0.5
	''''''
	url = "https://www.google.com.tr/imghp?hl=tr"
	timer = 1
	index = 0
	datas = []
	all_photos = {}

	def __init__(self):

		'''
			Constructor function.
		self.driver
		self.LAST_HEIGHT
		self.get()
		'''

		#self.driver = webdriver.Chrome("$HOME/bin/chromedriver") # for searching by google chrome.
		self.driver = webdriver.Firefox()
		self.driver.get(self.url)
		self.LAST_HEIGHT = self.driver.execute_script("return document.body.scrollHeight")

		self.Get() # taking datas

	def Get(self):
		print(f"Searching {search_input} photos on {self.driver.title}...")
		# sending keys 
		self.driver.find_element(by=By.XPATH ,value="/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input").send_keys(search_input)
		self.driver.find_element(by=By.CLASS_NAME, value="zgAlFc").click()
		refresh_site = self.driver.find_element(by=By.XPATH, value="//*[@id='islmp']/div/div/div/div[1]/div[2]/div[2]/input")

		try:
			while True:
				
				if refresh_site.is_displayed():
					refresh_site.click()

				self.datas = WebDriverWait(self.driver, 10).until(
						EC.presence_of_all_elements_located((By.TAG_NAME, "img"))
					) # finish taking datas

				time.sleep(2)
				time.sleep(self.SCROLL_PAUSE_TIME)

				self.driver.execute_script(f"window.scrollTo({self.timer}, document.body.scrollHeight);")
				NEW_HEIGHT = self.driver.execute_script("return document.body.scrollHeight")

				if NEW_HEIGHT == self.LAST_HEIGHT or self.timer == 15: # if you want to search photos more than, you can increase 'self.timer == {15}'.
					break

				self.timer = self.timer + 1

		except Exception as error:
			print("Some errors.", error)

		finally:
			print("Successfull!")

			self.Print() # Print function is calling.


	def Print(self):
		for data in self.datas[5:]:
			if data.get_attribute('src') is not None:
				self.all_photos[self.index] = data.get_attribute('src') # get links of all photos
				self.index = self.index + 1

		self.ToJson()

	
	def ToJson(self):
		with open("photos.json", "w") as f:
			f.write(json.dumps(self.all_photos, indent = 2)) # writing datas to json file

# finish

if __name__ == "__main__":
	input_data = OptionParser()
	input_data.add_option("-s", dest="search", default="profile photos")
	(option, args) = input_data.parse_args(sys.argv)
	search_input = option.search
	# subprocess.run(["pip", "install", "selenium"])
	Main()