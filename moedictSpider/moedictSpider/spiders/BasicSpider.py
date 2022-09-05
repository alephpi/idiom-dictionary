from ast import parse
import logging
import scrapy
import opencc
from tqdm import tqdm
from moedictSpider.items import MoedictSpiderItem
import json

converter_s2t = opencc.OpenCC('s2t.json')
converter_t2s = opencc.OpenCC('t2s.json')


class BasicSpider(scrapy.Spider):
    name = 'basic'

    def start_requests(self):
        with open('E:\WORKS\计算机\Python\idiom dictionary\moedictSpider\moedictSpider\spiders\多音成语表.json', 'r', encoding='utf-8') as file:
            dict_idiom = json.load(file)
        # moedict
        api = 'https://www.moedict.tw/uni/'
        for idiom in tqdm(dict_idiom.keys()):
            # convert to traditional chinese
            idiom_t = converter_s2t.convert(idiom)
            logging.info(idiom_t)
            url = api + idiom_t
            yield scrapy.Request(url, callback=self.parse, cb_kwargs=dict(idiom=idiom))

    def parse(self, response, idiom):
        item = MoedictSpiderItem()
        item['idiom'] = idiom
        logging.info(idiom)
        # if no such idiom in the dict
        if response.status == 404:
            # part1 = idiom_t[:2]
            # part2 = idiom_t[2:]
            return
        parsed = json.loads(response.text)
        logging.info(parsed)
        item['phone'] = parsed['heteronyms'][0]['pinyin']
        yield item
