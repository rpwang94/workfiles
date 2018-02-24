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
		source_page = getHtml(final_url)
		source_page = BeautifulSoup(source_page, 'html5lib')
		source_page = source_page.find_all('table', id='MainPH_MainPH_grdApplications_DXMainTable')
		if len(source_page) > 0:
			source_page = BeautifulSoup(str(source_page[0]), 'html5lib')
			source_tr = source_page.find_all('tr', class_='dxgvDataRow_FMecat dxgv-row')
			# print(source_tr[:1])
			for source_td in source_tr:
				source_td = source_td.find_all('td')
				app_list = []
				for source_txt in source_td:
					source_txt = source_txt.get_text()
					source_txt = re.sub('\\xa0',' ', source_txt)
					source_txt = re.sub('\n', ' ', source_txt)
					source_txt = re.sub('Qty\.', '',source_txt)
					source_txt = re.sub('\s{1,}', ' ', source_txt)
					app_list.append(source_txt)
				Make, Model, Year, position, wheel, qty, engine_base, vin, desg = app_list
				if re.match('(\d{4})-(\d{4})', Year):
					tot_year = re.match('(\d{4})-(\d{4})', Year)
					begin, end = tot_year.groups()
					for Year in range(int(end), int(begin)+1):
						write_file.write(str(part_type1) + ',' +str(part_number) + ',' + Make + ',' + str(Model) + ',' + str(Year) + ',' + position + ',' + wheel + ',' + str(qty) + ',' + engine_base + ',' + vin + ',' + desg + '\n')

file_name = str('Plus_C_to_K_Not_Found') + '.csv'
write_file = open(file_name, "w+")
write_file.write('part_type, part_number, make, model, year, position, wheel, qty, engine_base, VIN, Eng_des ' + '\n')

with open('Plus_C_to_Not_Found.csv', 'r') as f:
	i=0
	for line in f:
		part_num, description = line.split(',')
		parttocheck = part_num
		openTabs(parttocheck)
		i=i+1
		print(i)
		print(parttocheck)
	write_file.close()
