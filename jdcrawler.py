'''
Created on Sep 3, 2016

@author: chenli
'''
import urllib.request
import requests
from bs4 import BeautifulSoup
import os

class JDCrawler(object):
    __index = 2300000#商品起始ID
    __url = 'http://item.jd.com/'
    __urlPre = 'http://p.3.cn/prices/get?type=1&area=1_72_4139&pdtk=&pduid=1672389251&pdpin=&pdbp=0&skuid=J_'
    __urlNex = '&callback=cnp'
    __path = 'F:\pythonworkspace\download'
    __headers = {
        'Host': 'item.jd.com',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',

    }
    
    def __init__(self, sumValue):
        self.s = requests.Session()
        self.__sum = sumValue
        self.filedes = open(JDCrawler.__path + '\\desc.txt', 'w')
        
    def startDownload(self):
        flag = 0
        while flag < self.__sum:
            try:
                url = JDCrawler.__url + str(JDCrawler.__index) + ".html" 
                response = self.s.get(url, headers = JDCrawler.__headers)
                soup = BeautifulSoup(response.text,'html.parser')
                item = soup.body.find_all('img')[0]
                urlother = soup.find(text='商品介绍').parent['href']
                response = self.s.get(url + urlother, headers = JDCrawler.__headers)
                soup = BeautifulSoup(response.text,'html.parser')
                itemtype = soup.body.find_all(attrs={'class':'p-parameter-list'})[-1].find_all('li')[-1]['title']
                response = self.s.get(JDCrawler.__urlPre + str(JDCrawler.__index) + JDCrawler.__urlNex)
                price = eval(response.text.split('[')[1].split(']')[0])['p']
                if item['alt'] != None and item['src'] != None and itemtype != None and price != None:
                    urllib.request.urlretrieve('http:' + item['src'], os.path.join(JDCrawler.__path, str(JDCrawler.__index) + '.jpg'))
                    self.filedes.write(str(JDCrawler.__index) + '|' + str(itemtype) + '|' + str(item['alt']) + '|' + str(price) + '\n')#商品类型itemtype
                    flag +=1                    
            except Exception:
                pass
            JDCrawler.__index = JDCrawler.__index + 1;
        self.filedes.close()

if __name__ == '__main__':
    test = JDCrawler(10000)#初始化需要下载的条目数
    test.startDownload()