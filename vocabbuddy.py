import scrapy
from bs4 import BeautifulSoup as bs
import re
import os
import time
from scrapy.crawler import CrawlerProcess


pos_short = {'noun':'n.',
"verb":'v.',
"adjective":'adj.',
"adverb":'adv.',
"pronoun":"pron.",
"preposition":"prep.",
"conjunction":'conj.',
"interjection":'inter.'}

output =  open('output.txt','w',encoding="utf-8")


def getVocabs(page,vocab,output):
    if not page.status is 200:
        print('===Not in Dict===')
        return
    soup = bs(page.body,'html.parser')

    poses = [tag for tag in soup.find_all(class_='pos-header') if "runon-head" not in tag.parent['class']]
    for pos in poses:
        try:
            part_of_speech = '('+pos_short[pos.find(class_="pos").text]+' )'
        except:
            print("Something Weird Happened")
            continue
        pos_bodys = pos.find_next_siblings()[0]
        senses = [tag for tag in pos_bodys.find_all(class_='sense-block') if 'british' in tag['id']]    #sense means a definition, and I only apply for english def
        for sense in senses:
            defin = sense.find(class_="def").text #get definition
            defin = defin.replace(':','')
            try:
                examp = sense.find_all(class_="examp emphasized")[0].text
            except:
                print("===No Example===")
                output.write(vocab+part_of_speech+'\t'+part_of_speech+defin+';')
                continue

            output.write(vocab+part_of_speech+'\t'+part_of_speech+defin+'\n\ne.g. '+examp+';')
        print('--------------')
    print("End\n\n")


class Vocabscraper(scrapy.Spider):
    name = 'cambridge'

    custom_settings = {
        "DOWNLOAD_DELAY":0.5,
        "AUTOTHROTTLE_ENABLED":True,
        "AUTOTHROTTLE_START_DELAY":5,
        "AUTOTHROTTLE_MAX_DELAY":60,
        "AUTOTHROTTLE_TARGET_CONCURRENCY" : 1.0
    }
    DOWNLOADER_MIDDLEWARES = {
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
    }
    headers = {"User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"}

    def start_requests(self):
        urls = open('urls.txt').read().split()
        for url in urls:
            vocab = re.findall('english/([a-zA-z]+)',url)
            print("===Getting {}===".format(vocab))
            yield scrapy.Request(url=url, callback=self.parse,headers=self.headers)

    def parse(self, response):
        vocab = re.findall("/english/([a-zA-z]+)",response.url)[0]
        getVocabs(response,vocab,output)

spider = Vocabscraper()
process = CrawlerProcess()
process.crawl(spider)
process.start()

output.close()
