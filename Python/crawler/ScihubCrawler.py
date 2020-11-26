# -*- coding:utf-8 -*-
#@Time : 2020/11/25 0025 17:19
#@Author: Joword
#@File : ScihubCrawler.py

from selenium import webdriver
import time

def selenium_crawler():
	
	# 配置文件
	options = webdriver.ChromeOptions()
	print(dir(options))
	prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': 'G:\\'}
	options.add_experimental_option('prefs', prefs)
	
	# 下载模块
	chrome_driver = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
	driver = webdriver.Chrome(executable_path=chrome_driver,chrome_options=options)
	driver.get('https://sci-hub.do/')
	driver.find_element_by_name("request").send_keys("17553572")
	driver.find_element_by_id("open").click()
	driver.find_element_by_xpath('//*[@id="buttons"]/ul/li/a').click()
	time.sleep(5)
	driver.quit()
	
if __name__ == '__main__':
	test = selenium_crawler()