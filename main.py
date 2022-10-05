from selenium import webdriver
import urllib
import requests
import subprocess
from optparse import OptionParser
import sys
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Main:
	url = "https://www.google.com.tr/imghp?hl=tr"
	index = 0
	datas = []
	all_photos = {}
	def __init__(self):
		# self.driver = webdriver.Chrome(executable_path=r'chromedriver')
		self.driver = webdriver.Firefox()
		self.driver.get(self.url)

		self.Get() # taking datas

	def Get(self):
		print(self.driver.title)
		# sending keys 
		self.driver.find_element(by=By.XPATH ,value="/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input").send_keys(search_input)
		self.driver.find_element(by=By.CLASS_NAME, value="zgAlFc").click()

		try:
			while True:
				self.datas = WebDriverWait(self.driver, 10).until(
						EC.presence_of_all_elements_located((By.TAG_NAME, "img"))
					) # finish taking datas

				break

		except Exception as error:
			print("Some errors.", error)

		finally:
			print("Successfull!")

			self.Print() # Print function is calling.


	def Print(self):
		for data in self.datas[5:]:
			# print(data.get_attribute('src'), "\n")
			# print("*"*25)

			self.all_photos[self.index] = data.get_attribute('src')
			self.index = self.index + 1

		self.ToJson()

	
	def ToJson(self):
		with open("photos.json", "w") as f:
			f.write(json.dumps(self.all_photos, indent = 2))

# finish

if __name__ == "__main__":
	input_data = OptionParser()
	input_data.add_option("-s", dest="search", default="profile photos")
	(option, args) = input_data.parse_args(sys.argv)
	search_input = option.search
	# subprocess.run(["bash", ".dinstaller.sh"])
	Main()