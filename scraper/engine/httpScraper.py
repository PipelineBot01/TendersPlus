import json
import time
import pandas as pd
import requests
from lxml import etree
from db.mongoDB import mongo


class webScarper:
    def __init__(self, config, seed_url, url_head, parser_config, interval, save_mongo=True,
                 saveInfo=['asset/webScraperInfo', '.csv']) -> None:
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/86.0.4240.198 Safari/537.36 '
        }
        pass

    def get_urls(self) -> None:
        pass

    def run(self):
        pass

    def parser(self, url):
        pass

    def downloader(self, url):
        pass

    def save2Mongo(self, data):
        pass


class tenderScraper(webScarper):
    def __init__(self, config, seed_url, url_head, parser_config, tender_head, interval, save_mongo,
                 saveInfo=['results/historyInfo', '.csv']) -> None:
        super().__init__(config, seed_url, url_head, parser_config, interval, save_mongo, saveInfo)
        self.tenders = []
        self.tender_head = tender_head

    def get_urls(self) -> None:
        pages = [self.url_head]
        seed_html = self.downloader(self.seed_url)
        pageLink = seed_html.xpath('//*[@id="mainContent"]/div/div[4]/ul/li/a/@href')
        pageId = seed_html.xpath('//*[@id="mainContent"]/div/div[4]/ul/li/a/text()')
        for i in range(1, len(pageId) - 1):
            pages.append(self.url_head + pageLink[i - 1])

        tenders = {}
        for i in range(len(pages)):
            link = pages[i]
            html = self.downloader(link)
            links = html.xpath('//div[@class="list-desc-inner"]/a/@href')
            ids = html.xpath('//div[@class="list-desc-inner"]/a/text()')
            for j in range(0, len(ids), 2):
                print(ids[j])
                tenders[ids[j]] = self.tender_head + links[j]
            print("page " + str(i + 1) + " finished")

        try:
            jsObj = json.dumps(tenders)
            fileObject = open('./assets/tendersLink.json', 'w')
            self.url_collector = tenders
            fileObject.write(jsObj)
            print('save Link finished')
            fileObject.close()
        except Exception as e:
            print(e)
        time.sleep(self.interval)

    def downloader(self, url) -> str:
        response = requests.get(url, self.headers)
        tendersPage = response.text.encode('utf-8', 'ignore').decode('utf-8', 'ignore')
        return etree.HTML(tendersPage)

    def run(self, save_mongo=False):
        print('collecting urls')
        self.get_urls()
        linkDic = self.url_collector
        errorStuff = {}
        print("Parsing links")

        for tid, link in linkDic.items():
            print('Generate tender info', tid)
            try:
                tender = self.parser(link)
                self.tenders.append(tender)
                if save_mongo:
                    self.save2Mongo(tender)
            except Exception as e:
                print(e)
                print('-----> failed to scrap', tid)
                errorStuff.update({tid: link})
                continue
            time.sleep(self.interval)
        df = pd.DataFrame(self.tenders)
        print('Saving complete')
        try:
            jsObj = json.dumps(errorStuff)
            fileObject = open('assets/errorsLink.json', 'w')
            fileObject.write(jsObj)
            fileObject.close()
            print('Saving errorStuff complete')
        except Exception as e:
            print(e)
            print('Saving errorStuff failed')

    def parser(self, url) -> dict:
        parser_cfg = self.parser_config
        html = self.downloader(url)
        html = html.replace('<strong>', '')
        html = html.replace('</strong>', '')
        html = html.replace('\r\n', '')
        html = html.replace('  ', '')
        tree = etree.HTML(html)

        title = tree.xpath(parser_cfg.get('Title'))[0]
        labels = tree.xpath(parser_cfg.get('labels'))
        details = tree.xpath(parser_cfg.get('Details'))
        idx = 0
        attributes = {'Title': title, 'URL': url}
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
            ll = label.replace(":", "")
            attributes[ll] = info

        go = attributes
        return go

    def save2Mongo(self, tender):
        print('*******  insert tender info into database *********')
        mongodb = self.db
        result = mongodb.insert(tender)
        print('*******  finish tender info into database *********')


class goScraper(webScarper):
    def __init__(self, config, seed_url, url_head, go_head, parser_config, interval, save_mongo,
                 saveInfo=['results/historyInfo', '.csv']) -> None:
        super().__init__(config, seed_url, url_head, parser_config, interval, save_mongo, saveInfo)
        self.gos = []
        self.go_head = go_head

    def get_urls(self) -> None:
        pages = [self.url_head]
        seed_html = etree.HTML(self.downloader(self.seed_url))
        pageLink = seed_html.xpath('//*[@id="mainContent"]/div/div[3]/ul/li/a/@href')
        pageId = seed_html.xpath('//*[@id="mainContent"]/div/div[3]/ul/li/a/text()')
        for i in range(1, len(pageId) - 1):
            pages.append(self.url_head + pageLink[i - 1])

        gos = {}
        for i in range(len(pages)):
            link = pages[i]
            html = etree.HTML(self.downloader(link))
            links = html.xpath('//div[@class="list-desc-inner"]/a/@href')
            ids = html.xpath('//div[@class="list-desc-inner"]/a/text()')
            for j in range(0, len(ids), 2):
                gos[ids[j]] = self.go_head + links[j]
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
        self.get_urls()
        errorStuff = {}
        print("Parsing links")

        file_path = "./assets/gosLink.json"
        data = open(file_path, 'rb')
        linkDic = json.load(data)
        old_urls = pd.DataFrame(self.db.find_col("URL"))
        update_list = list(old_urls['URL'])
        gos_links = []
        for gid, link in linkDic.items():
            gos_links.append(link)

            print('Generate go info', gid)
            try:
                go = self.parser(link)
                self.gos.append(go)
                if self.save_mongo:
                    if link in update_list:
                        self.updateMongo(go)
                    else:
                        self.save2Mongo(go)
            except Exception as e:
                print(e)
                print('-----> failed to scrap', gid)
                errorStuff.update({gid: link})
                continue
            time.sleep(self.interval)
        df = pd.DataFrame(self.gos)
        for url in update_list:
            if url not in gos_links:
                self.db.delete(URL=url)
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

    def parser(self, url):
        config = self.parser_config
        html = self.downloader(url)
        html = html.replace('<strong>', '')
        html = html.replace('</strong>', '')
        html = html.replace('\r\n', '')
        html = html.replace('  ', '')
        tree = etree.HTML(html)

        title = tree.xpath(config.get('Title'))[0]
        labels = tree.xpath(config.get('labels'))
        details = tree.xpath(config.get('Details'))
        idx = 0
        attributes = {'Title': title, 'URL': url}
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
            ll = label.replace(":", "")
            attributes[ll] = info
        go = attributes
        return go

    def downloader(self, url) -> str:
        response = requests.get(url, self.headers)
        gosPage = response.text.encode('utf-8', 'ignore').decode('utf-8', 'ignore')
        return gosPage

    def save2Mongo(self, go):
        print('*******  insert tender info into database *********')
        mongodb = self.db
        result = mongodb.insert(go)
        print('*******  finish tender info into database *********')

    def updateMongo(self, go):
        print('*******  update tender info into database *********')
        mongodb = self.db
        q = {'URL': go['URL']}
        v = {'$set': go}
        result = mongodb.update_one(q, v)
