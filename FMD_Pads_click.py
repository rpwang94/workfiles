import time
import csv
import re
from bs4 import BeautifulSoup
import chardet
from selenium import webdriver
from urllib.request import urlopen
import requests
import os
from sqlalchemy import create_engine, Column, String, Table, MetaData, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
comma = ','
def getHtml(url):
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	header = {'User_Agent': user_agent}
	page = requests.get(url, headers=header)
	page.encoding = 'utf-8'
	return page.text


def openTabs(url):
	# driver=webdriver.Chrome('C:\Program Files (x86)\Python36-32\Scripts\chromedriver.exe')
	driver = webdriver.PhantomJS('C:\Program Files (x86)\Python36-32\Scripts\phantomjs.exe')
	driver.get(url)
	despage = driver.page_source
	page = BeautifulSoup(despage, 'html5lib')
	path_pre = "//tr[@id='"
	path_end = "']/td/img[@class='dxGridView_gvCollapsedButton_FMecat']"
	find_list = []
	finds = page.find_all('tr', class_='dxgvGroupRow_FMecat dxgv-grouprow')
	for row in finds:
		row_text = row.get_text()
		if "Disc Brake Pad Set" in row_text:
			row_id = row.get('id')
			find_list.append(row_id)
			path_mid = row_id
			finalpath = path_pre+path_mid+path_end
			finalpath = str(finalpath)
			ct_tr = driver.find_elements_by_xpath("//table[@id='MainPH_MainPH_grdPart_DXMainTable']/tbody")
			for ct_td in ct_tr:
				app_list = []
				ct_tr = driver.find_elements_by_xpath("//table[@id='MainPH_MainPH_grdPart_DXMainTable']/tbody")
				for pad_ct_tr in ct_tr:
					ct_td = pad_ct_tr.find_elements_by_xpath("//tr[@class='dxgvGroupRow_FMecat dxgv-grouprow']")
					# for pad_cunt_td in ct_td:
					# 	app_list.append(pad_ct_td.text)
				ct_td[1].find_element_by_xpath(finalpath).click()
				time.sleep(0.5)
				despage=driver.page_source
				Scrape(despage)
				time.sleep(3)
				des2 = driver.page_source
				page2 = BeautifulSoup(des2, 'html5lib')
				find2 = page.find_all('tr', class_='dxgvGroupRow_FMecat dxgv-grouprow')
				for bb in find2:
					bb_text = bb.get_text()
					bbtr = driver.find_elements_by_xpath("//table[@id='MainPH_MainPH_grdPart_DXMainTable']/tbody")
					for pad_bb_tr in bbtr:
						bb_td = pad_bb_tr.find_elements_by_xpath("//tr[@class='dxgvGroupRow_FMecat dxgv-grouprow']")
				bb_td[1].find_element_by_xpath("//tr[@rowtype='parttype-group']/td/img[@alt='[Collapse]']").click()
				time.sleep(0.5)
				print('found')
				time.sleep(0.5)
	driver.close()



def Scrape(despage):
	page = BeautifulSoup(despage, 'html5lib')
	page = page.find_all('tr', class_="dxgvDataRow_FMecat dxgv-row")
	def remove_html(html_file):
		text = BeautifulSoup(str(html_file), 'html.parser')
		text = text.get_text()
		# text = re.sub('{2,}\t','', text)
		return text
	for tr_data in page:
		brand_name = ''
		item = ''
		engine = ''
		vin = ''
		desg = ''
		drive =''
		subModel = ''
		position =''
		qualifiers = ''
		qty = ''
		page_list = []
		tr_data_1 = BeautifulSoup(str(tr_data), 'html.parser')
		tr_head = tr_data_1.find_all('td', class_="dxgv-part-link-td dxgv")
		tr_body = tr_data_1.find_all(class_="part-details dxgv")
		for head in tr_head:
			head = BeautifulSoup(str(head), 'html.parser')
			head_brand = head.find_all('div', class_="brand-lbl")
			head_item = head.find_all('a', class_="dxeHyperlink_FMecat dxgv-part-link")
			for head_1 in head_brand:
				brand_name = head_1.get_text().strip()
			for head_2 in head_item:
				item = head_2.get_text().strip()
		for body in tr_body:
			engine, vin, desg, drive, subModel, position, qualifiers, qty = tr_body
		engine = remove_html(engine)
		vin = remove_html(vin)
		desg = remove_html(desg)
		subModel = remove_html(subModel)
		position = remove_html(position)
		qualifiers = remove_html(qualifiers)
		drive = remove_html(drive)
		qty = remove_html(qty)
		qty = re.sub('\s', '', qty)
		# qty = re.search('(\d)',qty)
		# qty = qty.group(0)
		# print(qty)
		write_file.write(make + comma + model + comma + year + comma + str(brand_name) + comma + str(item) + comma + str(engine) + comma + str(vin) + comma + str(desg) + comma + str(drive) + comma + str(subModel) + comma + str(position) + comma + str(qualifiers) + comma + str(qty) +'\n')

file_name = str('20171109') + '.csv'
write_file = open(file_name, "w+")
write_file.write('make, model, year, brand, part, engine, vin, desg, drive, subModel, position, qualifiers, qty ' + '\n')

with open('links.csv', 'r') as f:
	i=0
	for line in f:
		make, model, year, link = line.split(',')
		LINK = 'http://www.fme-cat.com/Application.aspx?year=' + year + '&make=' + make + '&model=' + model + '&cat=Brake&ga=Y'
		openTabs(LINK)
		i=i+1
		print(i)
	write_file.close()
