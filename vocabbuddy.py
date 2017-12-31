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

def getVocabs(page):
    with open('output.txt','w',encoding="utf-8") as output:
        if not page.status is requests.codes.ok:
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
        "AUTOTHROTTLE_ENABLED":True,
        "AUTOTHROTTLE_START_DELAY":1,
        "AUTOTHROTTLE_MAX_DELAY":10,
    }
    DOWNLOADER_MIDDLEWARES = {
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
        'random_useragent.RandomUserAgentMiddleware': 400
    }


    def start_requests(self):
        urls = open('urls.txt').read().split()
        for url in urls:
            vocab = re.findall('english/([a-zA-z]+)',url)
            print("===Getting {}===".format(vocab))
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        getVocabs(response)

spider = Vocabscraper()
process = CrawlerProcess()
process.crawl(spider)
process.start()
