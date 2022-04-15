import json
from mimetypes import init
import os
import time
from datetime import date
from datetime import datetime
import pandas as pd
import requests
from lxml import etree
from mongoDB import mongo
import cfg

class webScarper():
    def __init__(self, config, seed_url, url_head, parser_config,  interval, save_mongo = True, saveInfo=['asset/webScraperInfo', '.csv']) -> None:
        self.config = config
        self.seed_url = seed_url
        self.saveInfo = saveInfo
        self.url_head = url_head
        self.interval = interval
        self.parser_config = parser_config
        self.url_collector = {}
        host, port, user, pwd, db, collection = self.config
        self.db = mongo(host, port, user, pwd, db, collection)
        self.save_mongo = save_mongo
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        }
        pass


    def get_urls(self) -> None:
        pass


    def run(self):
        pass

    def parser(self):
        pass


    def downloader(self):
        pass

    def save2Monogo(self):
        pass


class tenderScraper(webScarper):
    def __init__(self, config, seed_url, url_head, tender_head, interval, save_mongo, saveInfo=['results/historyInfo', '.csv']) -> None:
        super().__init__(config, seed_url, url_head, interval, save_mongo, saveInfo)
        self.tender_head = tender_head


    def get_urls(self) -> None:
        pages = []
        pages.append(self.url_head)
        pageLink = html.xpath('//*[@id="mainContent"]/div/div[4]/ul/li/a/@href')
        pageId = html.xpath('//*[@id="mainContent"]/div/div[4]/ul/li/a/text()')
        for i in range(1,len(pageId) - 1):
            pages.append(self.url_head + pageLink[i - 1])

        tenders = {}
        for i in range(len(pages)):
            link = pages[i]
            html  = self.downloader(link)
            links = html.xpath('//div[@class="list-desc-inner"]/a/@href')
            ids = html.xpath('//div[@class="list-desc-inner"]/a/text()')
            for i in range(0,len(ids),2):
                print (ids[i])
                tenders[ids[i]] = self.tender_head + links[i]
            print("page " + str(i + 1) + " finished")

        try:
            jsObj = json.dumps(tenders)
            fileObject = open('./assets/tendersLink.json', 'w')
            self.url_collector = tenders
            fileObject.write(jsObj)
            print('save Link finished')
            fileObject.close()
            self.links.clear()
        except Exception as e:
            print(e)
        time.sleep(self.interval)



    def downloader(self, url) -> str:
        response = requests.get(url, self.headers)
        tendersPage = response.text.encode('utf-8', 'ignore').decode('utf-8', 'ignore')
        return etree.HTML(tendersPage)

    def run(self, save_mongo = False):
        print('collecting urls')
        html = etree.HTML(self.downloader(self.seed_url, self.headers))
        self.get_urls(html)
        linkDic = self.url_collector
        errorStuff = {}
        print("Parsing links")

        for id, link in linkDic.items():
            print('Generate tender info', id)
            try:
                tender = self.parser(id, link)
                if save_mongo:
                    self.save2Monogo(tender)
            except Exception as e:
                print(e)
                print('-----> failed to scrap', id)
                errorStuff.update({id: link})
                continue
            time.sleep(self.interval)
        df = pd.DataFrame(self.tenders)
        print('Saving complete')
        try:
            jsObj = json.dumps(errorStuff)
            fileObject = open('assets/errorsLink.json', 'w')
            fileObject.write(jsObj)
            fileObject.close()
            self.links.clear()
            print('Saving errorStuff complete')
        except Exception as e:
            print(e)
            print('Saving errorStuff failed')


    def parser(self, id, url) -> dict:
        parser_cfg  = self.parser_config
        html = self.downloader(url)
        html = html.replace('<strong>', '')
        html = html.replace('</strong>', '')
        html = html.replace('\r\n','')
        html = html.replace('  ','')
        tree = etree.HTML(html)      

        title = tree.xpath(parser_cfg.get('Title'))[0]
        #contacts = tree.xpath(config.get('Contacts'))
        #while ":" in contacts: contacts.remove(":")
        labels = tree.xpath(parser_cfg.get('labels'))
        details = tree.xpath(parser_cfg.get('Details'))

        go = {}
        #contacts = tree.xpath(config.get('Contacts'))
        #while ":" in contacts: contacts.remove(":")
        idx = 0
        attributes={}
        # attributes['_id'] = id
        attributes['Title'] = title
        attributes['URL'] = url
        for i in range(len(labels)):
            label = labels[i]
            info = ''
            while idx < len(details):
                if details[idx] == label:
                    idx += 1
                elif details[idx] == ':':
                    idx += 1
                elif i < len(labels) - 1 and details[idx] == labels[i + 1]:
                    break
                else:
                    if info == '':
                        info = details[idx]
                    else:
                        info = info + " " + details[idx]
                    idx += 1
            l = label.replace(":","")
            attributes[l] = info


        go = attributes
        return go




    def save2Monogo(self, tender: dict[str:str]):
        print('*******  insert tender info database *********')
        mongodb = self.db
        result = mongodb.insert(tender)
        print('*******  finish tender info database *********')


class goScraper(webScarper):
    def __init__(self, config, seed_url, url_head, go_head, parser_config, interval, save_mongo, saveInfo=['results/historyInfo', '.csv']) -> None:
        super().__init__(config, seed_url, url_head, parser_config, interval, save_mongo, saveInfo)
        self.go_head = go_head

    def get_urls(self) -> None:
        pages = []
        pages.append(self.url_head)
        pageLink = html.xpath('//*[@id="mainContent"]/div/div[4]/ul/li/a/@href')
        pageId = html.xpath('//*[@id="mainContent"]/div/div[4]/ul/li/a/text()')
        for i in range(1,len(pageId) - 1):
            pages.append(self.url_head + pageLink[i - 1])

        gos = {}
        for i in range(len(pages)):
            link = pages[i]
            html  = self.downloader(link)
            links = html.xpath('//div[@class="list-desc-inner"]/a/@href')
            ids = html.xpath('//div[@class="list-desc-inner"]/a/text()')
            for i in range(0,len(ids),2):
                print (ids[i])
                gos[ids[i]] = self.tender_head + links[i]
            print("page " + str(i + 1) + " finished")

        try:
            jsObj = json.dumps(gos)
            fileObject = open('./assets/gosLink.json', 'w')
            self.url_collector = gos
            fileObject.write(jsObj)
            print('save gos Link finished')
            fileObject.close()
            self.url_collector.clear()
        except Exception as e:
            print(e)
        time.sleep(self.interval)


    def run(self):
        print('collecting urls')
        html = etree.HTML(self.downloader(self.seed_url, self.headers))
        self.get_urls(html)
        linkDic = self.url_collector
        errorStuff = {}
        print("Parsing links")

        for id, link in linkDic.items():
            print('Generate go info', id)
            try:
                go = self.parser(id, link)
                if self.save_mongo:
                    self.save2Monogo(go)
            except Exception as e:
                print(e)
                print('-----> failed to scrap', id)
                errorStuff.update({id: link})
                continue
            time.sleep(self.interval)
        df = pd.DataFrame(self.tenders)
        print('Saving complete')
        try:
            jsObj = json.dumps(errorStuff)
            fileObject = open('assets/errorsLink.json', 'w')
            fileObject.write(jsObj)
            fileObject.close()
            self.url_collector.clear()
            print('Saving errorStuff complete')
        except Exception as e:
            print(e)
            print('Saving errorStuff failed')

    
    def parser(self):
        return super().parser()

    def downloader(self, url) -> str:
        response = requests.get(url, self.headers)
        tendersPage = response.text.encode('utf-8', 'ignore').decode('utf-8', 'ignore')
        return etree.HTML(tendersPage)

    def save2Monogo(self, go: dict[str:str]):
        print('*******  insert tender info database *********')
        mongodb = self.db
        result = mongodb.insert(go)
        print('*******  finish tender info database *********')