import json
import os
import time

import pandas as pd
import requests
from lxml import etree

class tenderScraper():
    def __init__(self, url, interval, saveInfo=['results/tendersInfo', '.csv'], config=None):
        '''
        :param url: web url
        :param interval: time interval between visiting each link
        :param saveInfo: ['saving path','saving format']
        :param config config file for re
        :var links {stuff name: web page url}
        '''
        self.url = url
        self.interval = interval
        self.saveInfo = saveInfo
        self.links = {}
        self.tenders = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        }

        # setting socks5 proxy
        #self.proxy = {"http": "socks5://127.0.0.1:10808", "https": "socks5://127.0.0.1:10808"}
        #self.config = {}

    def loadConfig(self):
        '''
        Loading config file for re compile key words
        :return:
        '''
        return None


    def get_TendersLink(self, html, tenders):
    
        head = "https://www.tenders.gov.au"
        links = html.xpath('//div[@class="list-desc-inner"]/a/@href')
        ids = html.xpath('//div[@class="list-desc-inner"]/a/text()')
        for i in range(0,len(ids),2):
            tenders[ids[i]] = head+links[i]
        return tenders



    def getLinks(self, html):
        '''
        :return: list with links on the page
        '''
        urlHead = "https://www.tenders.gov.au/Atm/"
        pages = []
        pages.append(urlHead)
        pageLink = html.xpath('//*[@id="mainContent"]/div/div[4]/ul/li/a/@href')
        pageId = html.xpath('//*[@id="mainContent"]/div/div[4]/ul/li/a/text()')
        for i in range(1,len(pageId) - 1):
            #print(pageId[i])
            pages.append(urlHead + pageLink[i - 1])


        tenders = {}
        for i in range(len(pages)):
            link = pages[i]
            response = requests.get(link)
            tendersPage = response.text.encode('utf-8', 'ignore').decode('utf-8', 'ignore')
            html  = etree.HTML(tendersPage)
            tenders = self.get_TendersLink(html,tenders)
            print("page " + str(i + 1) + " finished")

        try:
            jsObj = json.dumps(tenders)
            fileObject = open('results/tendersLink.json', 'a')
            fileObject.write(jsObj)
            fileObject.close()
            self.links.clear()
        except Exception as e:
            print(e)
        time.sleep(self.interval)
    
    
    def run(self):
        # print('Loading config file')
        # self.loadConfig()
        # print('Loading succeed')
        
        # print('Asking url')
        
        # response = requests.get(url=self.url, headers=self.headers)
        # html = etree.HTML(response.text)
        
        # self.getLinks(html)
        # self.cleanFormat()
        print("Parsing links")
        data = open("results/tendersLink.json", 'rb')
        linkDic = json.load(data)

        # if os.path.exists(''.join(i for i in self.saveInfo)):
        #     review = pd.read_csv(''.join(i for i in self.saveInfo))
        #     nameList = review.Name.unique()
        #     for i in nameList:
        #         if i in linkDic.keys():
        #             linkDic.pop(i)
        # else:
        
        errorStuff = {}
        for id, link in linkDic.items():
            print('Generate tender info', id)
            try:
                tender = self.scrape_tender(id, link)
            except Exception as e:
                print(e)
                print('-----> failed to scrap', id)
                errorStuff.update({id: link})
                continue
            time.sleep(self.interval)
            #print('Saving tender info')
        df = pd.DataFrame(self.tenders)
        
        re = self.saveStuffInfo(df)
        if not re:
            print('Save failed')
            print('-----> failed to scrap', id)
            errorStuff.update({id: link})
        print('Saving complete')
        try:
            jsObj = json.dumps(errorStuff)
            fileObject = open('results/errorTenders.json', 'w')
            fileObject.write(jsObj)
            fileObject.close()
            self.links.clear()
            print('Saving errorStuff complete')
        except Exception as e:
            print(e)
            print('Saving errorStuff failed')


    
    def scrape_tender(self, id, url):
        config = {
            'Contacts': '//*[@class = "pc"]//*[@class="contact-long"]//*/text()',
            'Name': '//*[@class="lead"]/text()',
            'labels': '//*[@id="mainContent"]/div/div[2]/div[2]/div[1]//*/label/text()',
            'Details': '//*[@id="mainContent"]/div/div[2]/div[2]/div[1]//*/text()'
        }
        response = requests.get(url, headers=self.headers)
        html = response.text.encode('utf-8', 'ignore').decode('utf-8', 'ignore')
        html = html.replace('<strong>', '')
        html = html.replace('</strong>', '')
        html = html.replace('\r\n','')
        html = html.replace('  ','')
        tree = etree.HTML(html)

        tender = {}
        name = tree.xpath(config.get('Name'))[0]
        #contacts = tree.xpath(config.get('Contacts'))
        #while ":" in contacts: contacts.remove(":") 
        labels = tree.xpath(config.get('labels'))
        details = tree.xpath(config.get('Details'))
        idx = 0
        attributes={}
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

            attributes[label] = info
        tender["Name"] = name
        tender["ID"] = id
        # for i in range(0, len(contacts),2):
        #     tender[contacts[i]] = contacts[i+1]
        tender["attributes"] = attributes
        self.tenders.append(tender)
        return tender

        # attributes

    def saveStuffInfo(self, df):
        '''
        :return: True if successfully saved, otherwise False
        '''
        localPath, format = self.saveInfo
        if format == '.csv':
            try:
                df.to_csv(localPath + '.csv', mode='a', index=False)
            except Exception as e:
                print(e)
                return False
        return True