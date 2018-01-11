import scrapy 
from bs4 import BeautifulSoup as bs
from scrapy.crawler import CrawlerProcess

class PttSpider(scrapy.Spider):
    name = 'ptt'
    def start_request(self):
        url = "https://www.ptt.cc/bbs/C_Chat/index.html"
        yield scrapy.Requests(url = url, callback = self.parseIndex)
    
    def parseIndex(self, response):
        soup = bs(response.body)
        titles = soup.find_all(class_="title")
        for title in titles:
            url = title.findChildren()[0]['href']
            url = url.replace('/bbs','https://www.ptt.cc')
            print(url)
            yield scrapy.Requests(url = url, callback = self.parsePage)
        
        try:
            next_page = soup.find_all(text="上頁")['href']
            yield scrapy.Requests(url=next_page, callback = self.parseIndex)
        except:
            print("Session end.")
        
                           
        
    def parsePage(self,response):
        soup = bs(response.body,'html.parser')
        title = soup.find(property="og:title")['content']
        arthor = soup.find(property="og:article-meta-value").getText()
        
        print("title: {}, arthor: {}".format(title,arthor))
        

process = CrawlerProcess()
process.crawl(PttSpider)
process.start()