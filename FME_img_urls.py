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


def openTabs(parttocheck):
	part_number = parttocheck
	main_url = 'http://www.fme-cat.com'
	url = 'http://www.fme-cat.com/PartInterchange.aspx?pn='+part_number
	html = getHtml(url)
	html = BeautifulSoup(html, 'html5lib')
	search_result = html.find_all('span', id='MainPH_MainPH_Label_Part')
	search_result1 = search_result[0].get_text()
	table_id = html.find_all('div', id='MainPH_MainPH_Panel_OurParts')
	if len(table_id) > 0:
		part_type = html.find_all('span', id='MainPH_MainPH_grdPart_lblProdType_0')
		part_type1 = part_type[0].get_text()
		type_list = []
		type_list.append(part_type1)
		html = html.find_all('a', id='MainPH_MainPH_grdPart_hlPartNumber_0')
		part_url = html[0].get('url')
		final_url = main_url + part_url
		detail_page = getHtml(final_url)
		detail_page = BeautifulSoup(detail_page, 'html5lib')
		detail_page = detail_page.find_all('img', style="max-width: 100%")
		for img_link in detail_page:
			img_link = detail_page[0].get("src")
			url_list=[]
			url_list.append(img_link)
			print(img_link)
			write_file.write(str(part_type1) + ',' +str(part_number) + ',' + img_link + '\n')

file_name = str('picurls') + '.csv'
write_file = open(file_name, "w+")
write_file.write('part_type, part_number, url' + '\n')

with open('List.csv', 'r') as f:
	i=0
	for line in f:
		part_num, description = line.split(',')
		parttocheck = part_num
		openTabs(parttocheck)
		i=i+1
		print(i)
		print(parttocheck)
	write_file.close()
