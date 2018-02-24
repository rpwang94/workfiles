import csv
import re
import urllib
from urllib.request import urlopen
import requests
import os
from sqlalchemy import create_engine, Column, String, Table, MetaData, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

def getHtml(url):
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	header = {'User_Agent': user_agent}
	page = requests.get(url, headers=header)
	page.encoding = 'utf-8'
	return page.text


def download_pics(linkmate):
	pic_name = cbkn + '.jpg'
	urllib.request.urlretrieve(linkmate, pic_name)



with open('pictest.csv', 'r') as f:
	i=0
	for line in f:
		type, moog_n, link, sel, seq, cbkn, f_n = line.split(',')
		piclink = link
		download_pics(piclink)
		i=i+1
		print(i)
		print(cbkn)
