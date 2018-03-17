# -*- coding:utf-8 -*-

import requests,sys
from bs4 import BeautifulSoup

"""
网站: 笔趣看@www.biqukan.com
小说：篮球皇帝
"""

class downloader(object):
	def __init__(self):
		self.site = 'http://www.biqukan.com'
		self.url = 'http://www.biqukan.com/11_11214/' # 小说地址
		self.txtName = ''
		self.info = []  #小说基本信息
		self.names = []  #存放章节名
		self.urls = []  #存放章节链接
		self.nums = 0  #章节数

	def get_download_url(self):
		req = requests.get(url = self.url)
		html = req.text
		div_bf = BeautifulSoup(html,"lxml")
		listmain = div_bf.find_all('div',class_ = 'listmain')
		info = div_bf.find_all('div',class_ = "info")
		a = BeautifulSoup(str(listmain[0]),"lxml").find_all('a')
		span = BeautifulSoup(str(info[0]),"lxml").find_all('span')
		txtname = BeautifulSoup(str(info[0]),"lxml").find_all('h2')
		self.txtName = txtname[0].string
		for x in span[:5]:
			self.info.append(x.string)
		self.nums = len(a[12:448])
		for each in a[12:448]: # a[12:448] : 过滤掉 'listmain' 头部的最新章节列表 （按不同小说调整）
			self.names.append(each.string)
			self.urls.append(self.site + each.get('href'))

	def get_contents(self, url):
		req = requests.get(url = url)
		html = req.text
		bf = BeautifulSoup(html, 'lxml')
		texts = bf.find_all('div',class_ = "showtxt")
		texts = texts[0].text.replace('\xa0'*8,'\n\n').replace(url + '　　请记住本书首发域名：www.biqukan.com。笔趣阁手机版阅读网址：m.biqukan.com','')
		return texts

	def writer(self,name,path,text):
		with open(path,'a',encoding='utf-8') as f:
			f.write(name)
			f.writelines(text)
			f.write('\n\n')

if __name__ == '__main__':
	dl = downloader()
	dl.get_download_url()
	with open(dl.txtName + '.txt','a',encoding='utf-8') as f:
		f.write(dl.txtName + '\n')
		for x in dl.info:
			f.write(x + '\n')
		f.write('\n\n')
	
	print('开始下载...')
	for i in range(dl.nums):
		dl.writer(dl.names[i],dl.txtName + '.txt',dl.get_contents(dl.urls[i]))
		sys.stdout.write("已下载：%.3f%%" % float(i / dl.nums * 100) + '\r')
		sys.stdout.flush()
	f.close()
	print("下载完成！")