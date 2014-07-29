#coding:utf-8
import urllib2
import sqlite3
from bs4 import BeautifulSoup

class SpiderRobost:
	def __init__(self, args):
		self.args = args
		self.conn = None
		self.cur = None
		self.opener = urllib2.build_opener()
		self.headers = {
		    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:10.0.1) Gecko/20100101 Firefox/10.0.1'
		}
		self.opener.addheaders = self.headers.items()
		self.initDB()

	def getPage(self, address):
		content = self.opener.open(address).read()
		return content

	def getPageNumber(self):
		address = self.args["spider_content_object_page"]
		content = self.opener.open(address).read()
		soup = BeautifulSoup(content)
		title = soup.find("div", {"class": "pagebar"}).findAll("a")[-2]["title"]
		title = title.encode("utf8")
		page_num = title[3:len(title)-3]
		return int(page_num)

	def extractContent(self):
		page_num = self.getPageNumber()
		inserts = []
		for j in range(page_num):
			print "page%d" % (j+1)
			y = j + 1
			address = "http://www.qiushibaike.com/8hr/page/" + str(y)
			content = self.getPage(address)
			soup = BeautifulSoup(content)
			all_episodes = soup.findAll("div", id=lambda x: x and x.startswith('qiushi_tag_'))
			for i in range(len(all_episodes)):
				episode_to_be_handled = all_episodes[i]
				script = episode_to_be_handled.find("div", {"class": "content"})
				if script != None:
					script = script.string
				else:
					script = None
				img_url = episode_to_be_handled.findAll("img")
				if len(img_url) > 1:
					img_url = img_url[1]
				else:
					img_url = None
				if img_url != None:
					img_url = img_url["src"]
				else:
					img_url = "#"
				inserts.append((script, img_url))
		self.cur.executemany("insert into Episode values (?, ?)", inserts)
		self.conn.commit()

	def getDataFromDB(self):
		sql = '''
		  select * from Episode
		'''
		self.cur.execute(sql)
		res = []
		for row in self.cur:
			res.append(row)
		return res

	def closeDB(self):
		self.cur.close()

	def clearDB(self):
		sql = '''
		    delete from Episode
		'''
		self.cur.execute(sql)
		self.conn.commit()

	def initDB(self):
		self.conn = sqlite3.connect('data.db')
		self.cur = self.conn.cursor()
		sql = '''create table if not exists Episode (
		    script text,
		    url string)'''
		self.cur.execute(sql)
		self.conn.commit()

if __name__ == "__main__":
	args = {
	    "spider_content_object_page": "http://www.qiushibaike.com/"
	}
	sr = SpiderRobost(args)
	sr.clearDB()
	#sr.extractContent()
	sr.getDataFromDB()
	sr.closeDB()