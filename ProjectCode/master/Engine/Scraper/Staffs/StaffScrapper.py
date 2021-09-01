import json
import os
import time

import pandas as pd
import requests
from lxml import etree


class staffScraper():
    def __init__(self, url, interval, saveInfo=['../../assets/ScraperResult/ScraperResult_UC', '.csv'], config=None):
        '''
        :param url: web url
        :param interval: time interval between visiting each link
        :param saveInfo: ['saving path','saving format']
        :param config config file for re
        :var links {staff name: web page url}
        '''
        self.url = url
        self.interval = interval
        self.saveInfo = saveInfo
        self.links = {}
        self.staffs = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        }

        # setting socks5 proxy
        self.proxy = {"http": "socks5://127.0.0.1:10808", "https": "socks5://127.0.0.1:10808"}
        self.config = {}

    def loadConfig(self):
        '''
        Loading config file for re compile key words
        :return:
        '''
        return None

    def run(self):

        print('Loading config file')
        self.loadConfig()
        print('Loading succeed')

        print('Asking url')

        response = requests.get(url=self.url, headers=self.headers, proxies=self.proxy)
        html = response.text

        self.getLinks(html)
        self.cleanFormat()

        print('Parsing links')

        data = open("../../assets/ScraperResult/staffLink_UC.json", 'rb')
        linkDic = json.load(data)

        if os.path.exists(''.join(i for i in self.saveInfo)):
            review = pd.read_csv(''.join(i for i in self.saveInfo))
            nameList = review.Name.unique()
            for i in nameList:
                if i in linkDic.keys():
                    linkDic.pop(i)
        else:
            df_example = pd.DataFrame(None, columns=['Name', 'Email', 'OtherEmails', 'University', 'Colleges', 'Title',
                                                     'Profile',
                                                     'staffTags', 'ProjectTags'])
            df_example.to_csv(''.join(i for i in self.saveInfo), index=False)

        errorstaff = {}
        for name, link in linkDic.items():
            print('Generate staff info', name)
            try:
                staff = self.scrappingUrl(name, link)
            except Exception as e:
                print(e)
                print('-----> failed to scrap', name)
                errorstaff.update({name: link})
                continue
            time.sleep(self.interval)
            print('Saving staff info')
            re = self.savestaffInfo(staff)
            if not re:
                print('Save failed')
                print('-----> failed to scrap', name)
                errorstaff.update({name: link})
            print('Saving complete')

        print('Saving errorstaff')
        try:
            jsObj = json.dumps(errorstaff)
            fileObject = open('../../assets/ScraperResult/oldPage/errorstaff_UC.json', 'w')
            fileObject.write(jsObj)
            fileObject.close()
            self.links.clear()
            print('Saving errorstaff complete')
        except Exception as e:
            print(e)
            print('Saving errorstaff failed')

    def cleanFormat(self):
        data = open("../../assets/ScraperResult/oldPage/staffLink_UC.json", 'r+')
        tempStr = data.readlines()[0]
        tempStr = tempStr.replace('}{', ',')
        tempStr = tempStr.replace(',}', '}')
        fileObject = open('../../assets/ScraperResult/oldPage/staffLink_UC.json', 'w')
        fileObject.write(tempStr)
        fileObject.close()

    def getLinks(self, html):
        '''
        :return: list with links on the page
        '''
        urlHead = 'https://researchprofiles.canberra.edu.au/en/persons/?format=&page='
        tree = etree.HTML(html)
        index = tree.xpath('//nav[@class="pages"]/ul/li/a/text()')[-2]
        for link in range(int(index) + 1):
            url = urlHead + str(link)
            response = requests.get(url, headers=self.headers, proxies=self.proxy)
            staffPage = response.text.encode('utf-8', 'ignore').decode('utf-8', 'ignore')
            tree = etree.HTML(staffPage)
            staffUrl = tree.xpath('//a[@rel="Person"]/@href')
            staffName = tree.xpath('//a[@rel="Person"]/span/text()')
            for i in range(len(staffName)):
                print('save staff', staffName[i])
                l = staffUrl[i]
                self.links.update({staffName[i]: l})

            # save in json file with append operation
            print(self.links)
            try:
                jsObj = json.dumps(self.links)
                fileObject = open('../../assets/ScraperResult/staffLink_UC.json', 'a')
                fileObject.write(jsObj)
                fileObject.close()
                self.links.clear()
            except Exception as e:
                print(e)
            time.sleep(self.interval)

    def reformatInf(self, list):
        if len(list) != 0:
            text = list[0]
            text.replace('\n', '')
            text = text.replace(u'\xa0', u'')
            text = text.replace('\n', ' ')
            text = text.replace('\t', ' ')
        return text

    def extractStr(self, tree, parsing):
        interests = tree.xpath(parsing)
        if len(interests) != 0:
            try:
                interests = interests[0].xpath('string(.)').strip()
            except:
                interests = interests[0]
            interests = interests.replace('\n', '')
            interests = interests.replace('\r', '')
            interests = interests.replace('\xa0', '')
            return interests
        return ''

    def scrappingUrl(self, name, url):
        '''
        :return: staff info from this webpage
        '''
        config = {'Email': '//li[@class="emails"]/span/a/@href',
                  'Title': '//span[@class="job-title"]/text()',
                  'Organisation': '//a[@rel="Organisation"]/span/text()',
                  'Details': '//a[@class="portal_link btn-primary btn-large"]/@href',
                  'Tag': '//span[@class="concept"]/text()',
                  'TagWeight': '//span[@class="value sr-only"]/text()',
                  'Profile': '//div[@class="textblock"]',
                  'FingerPrintSection':'//section[@class="page-section content-relation-section person-fingerprint"]/div/ul/li/button/span/span',
                  'ProjectSection': '//div[@class="relation-list relation-list-publications"]/ul/li/div/ul/li/button/span/span'
                  }
        response = requests.get(url, headers=self.headers, proxies=self.proxy)
        html = response.text.encode('utf-8', 'ignore').decode('utf-8', 'ignore')
        html = html.replace('<strong>', '')
        html = html.replace('</strong>', '')
        tree = etree.HTML(html)

        email = tree.xpath(config.get('Email'))
        title = tree.xpath(config.get('Title'))
        if len(title) != 0:
            title = title[0]
        else:
            title = ''
        organisation = tree.xpath(config.get('Organisation'))
        if len(organisation) != 0:
            organisation = organisation[0]
        else:
            organisation = ''

        profile = tree.xpath(config.get('Profile'))
        if len(profile) != 0:
            try:
                profile = profile[0].xpath('string(.)').strip()
            except:
                profile = profile[0]
            profile = profile.replace('\n', '')
            profile = profile.replace('\t', '')
            profile = profile.replace('\r', '')
            profile = profile.replace('\xa0', '')
        else:
            profile = ''

        staffTags = self.getTags(tree, config, 'Details', 'fingerprint', 'Tag', 'TagWeight')
        if staffTags==None:
            staffTags=self.getDirectTags(tree,config,'FingerPrintSection', 'Tag', 'TagWeight')

        projectTags = self.getTags(tree, config, 'Details', 'publications', 'Tag', 'TagWeight')
        if projectTags==None:
            projectTags=self.getDirectTags(tree,config,'ProjectSection', 'Tag', 'TagWeight')

        param = {'University': 'Canberra',
                 'Colleges': organisation,
                 'Title': title,
                 "Profile": profile,
                 'staffTags': staffTags,
                 'ProjectTags': projectTags}

        from Staff import staff
        staff = staff(email, name, param)
        self.staffs.append(staff)
        return staff

    def getDirectTags(self,tree,config,title,title1,title2):
        tags={}
        projectTags = tree.xpath(config.get(title))
        if len(projectTags)==0: return {}
        name = projectTags[0].xpath(config.get(title1))
        weight = projectTags[0].xpath(config.get(title2))
        for i in range(len(name)):
            tags.update({name[i]:weight[i]})
        return tags

    def getTags(self, tree, config, title, title2, title3, title4):
        urlHead = 'https://researchprofiles.canberra.edu.au'
        fingerPrintUrl = tree.xpath(config.get(title))
        Url=''
        for i in fingerPrintUrl:
                if title2 in i:
                    Url = i
        if Url=='' or len(fingerPrintUrl)==0:
            return None
        fingerPrint = requests.get(urlHead + Url, headers=self.headers, proxies=self.proxy)
        fingerPrint = fingerPrint.text
        fingerPrint = etree.HTML(fingerPrint)
        tags = fingerPrint.xpath(config.get(title3))
        weights = fingerPrint.xpath(config.get(title4))
        staffTags = {}
        for i in range(len(tags)):
            tag = tags[i]
            weight = weights[i]
            staffTags.update({tag: weight})
        return staffTags

    def getGroup(self, head, proTitle, proUrls, project):
        for index in range(len(proTitle)):
            p = proTitle[index].encode('gbk', 'ignore').decode()
            proUrl = head + proUrls[index]
            project.update({p: proUrl})
        return project

    def savestaffInfo(self, staff):
        '''
        :return: True if successfully saved, otherwise False
        '''
        localPath, format = self.saveInfo
        if format == '.csv':
            try:
                pd.DataFrame(staff.output(), index=[0]).to_csv(localPath + '.csv', mode='a', header=None, index=False)
            except Exception as e:
                print(e)
                return False
        return True
