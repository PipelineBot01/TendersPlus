"""
Data scrapper for UC staffs, will read the config info from init file, saving the final scraping result into mongoDB

Authors:
- Leyang Chai u7201445
"""

import json
import os
import time
from datetime import date
import pandas as pd
import requests
from lxml import etree
from . import config,Staff,cfg,mongo




class UC_plug():

    def __init__(self, interval=3, saveInfo=None, proxy=None):
        '''
        Constructor, setting basic attributes and proxy.

        :param interval: time interval between visiting each link
        :param proxy: proxy config, only use for vpn
        '''

        # hard code
        self.url = config['url']
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        }

        self.interval = interval
        self.saveInfo = saveInfo
        # setting socks5 proxy
        self.proxy = proxy

        # dict: {key: username, value: userUrl}
        # program will automatically fill the suffix if username is not unique
        self.links = {}

        # list, saving staff object
        self.staffs = []

    def getLinks(self):
        '''
        This function will get all the sub links from the main website (e.g., page 1-10), then for each
        page, scrapping the staff info inside and saving the final result as format {key: username, value: userUrl}.
        Scrapping result will be save into "tempResult/staffLink_UC.json"

        '''

        # creating saving file dir
        isExists = os.path.exists("tempResult")
        if not isExists: os.makedirs("tempResult")
        if os.path.exists("tempResult/staffLink_UC.json"):
            os.remove('tempResult/staffLink_UC.json')

        response = requests.get(url=self.url, headers=self.headers, proxies=self.proxy)
        html = response.text

        tree = etree.HTML(html)
        index = tree.xpath(config['pageNav'])[-2]
        for link in range(int(index) + 1):
            url = config['urlHead'] + str(link)
            response = requests.get(url, headers=self.headers, proxies=self.proxy)
            staffPage = response.text.encode('utf-8', 'ignore').decode('utf-8', 'ignore')
            tree = etree.HTML(staffPage)
            staffUrl = tree.xpath(config['staffUrl'])
            staffName = tree.xpath(config['staffName'])
            for i in range(len(staffName)):
                print('save staff', staffName[i])
                tempUrl = staffUrl[i]

                # handle duplicated staff name
                while staffName[i] in self.links.keys(): staffName[i] += '*'
                self.links.update({staffName[i]: tempUrl})

            # saving staff links into local json file
            print(self.links)
            try:
                jsObj = json.dumps(self.links)
                fileObject = open('tempResult/staffLink_UC.json', 'a')
                fileObject.write(jsObj)
                fileObject.close()
                self.links.clear()
            except Exception as e:
                print(e)
            time.sleep(self.interval)
            self.cleanFormat()

    def checkCurrentFile(self, linkDic):
        '''
        This function will check the content in current staffLink_UC file and delete the existing user url
        from staff link dict in order to reduce duplicated scrapping work.
        :param linkDic: dict will staff name: staff url
        :return: the linkDic after filtering the duplicated info
        '''

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
        return linkDic

    def getUserInfo(self):
        '''
        This function will control the scrapping and saving process for each staff and call scrappingUrl to scrap the
        detail info. When any error occur in the scrapping process, the current staff will not be scrapped, name and
        url of this staff will be saved into a local json file named errorstaff_UC.
        '''

        data = open("tempResult/staffLink_UC.json", 'rb')

        linkDic = json.load(data)
        if (not self.saveInfo == None): linkDic = self.checkCurrentFile(linkDic)

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
            if (not self.saveInfo == None):
                print('Saving staff info to local')
                re = self.savestaffInfo(staff)
                if not re:
                    print('Save failed')
                    print('-----> failed to scrap', name)
                    errorstaff.update({name: link})
            # todo: save info into MongoDb
            print('Saving complete')
        print('Saving error staff')
        try:
            jsObj = json.dumps(errorstaff)
            fileObject = open('tempResult/errorstaff_UC.json', 'w')
            fileObject.write(jsObj)
            fileObject.close()
            self.links.clear()
            print('Saving error staff complete')
        except Exception as e:
            print(e)
            print('Saving error staff failed')

    def cleanFormat(self):
        '''
        Reset the format of staffLink_UC in order to avoid potential risks (e.g., double "{" or "}")
        '''

        data = open("tempResult/staffLink_UC.json", 'r+')
        tempStr = data.readlines()[0]
        data.close()
        tempStr = tempStr.replace('}{', ',')
        tempStr = tempStr.replace(',}', '}')

        fileObject = open('tempResult/staffLink_UC.json', 'w')
        fileObject.write(tempStr)
        fileObject.close()

    def reformatInf(self, list):
        '''
        Handling the messy code in text-based variable

        :param list: scrapping result, usually in [text] format
        :return: the cleaned text-based variable
        '''
        if len(list) != 0:
            text = list[0]
            text.replace('\n', '')
            text = text.replace(u'\xa0', u'')
            text = text.replace('\n', ' ')
            text = text.replace('\t', ' ')
        return text

    def extractStr(self, tree, parsing):
        '''
        Scrapping the strings from webpage, mainly for handling strings that are split in several paragraphs

        :param tree: XML object
        :param parsing: parsing standards, getting from config variable
        :return: a reformat text if there exist text, otherwise return empty string
        '''

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
        This function will scrap the detail staff in each staff links, scrapping result will be converted
        into a staff object and save in list.

        :return: staff info from this webpage
        '''

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
        if staffTags == None:
            staffTags = self.getDirectTags(tree, config, 'FingerPrintSection', 'Tag', 'TagWeight')

        projectTags = self.getTags(tree, config, 'Details', 'publications', 'Tag', 'TagWeight')
        if projectTags == None:
            projectTags = self.getDirectTags(tree, config, 'ProjectSection', 'Tag', 'TagWeight')

        param = {'University': 'Canberra',
                 'Colleges': organisation,
                 'Title': title,
                 "Profile": profile,
                 'staffTags': staffTags,
                 'ProjectTags': projectTags}

        staff = Staff(email, name, param)
        self.staffs.append(staff)
        return staff

    def getDirectTags(self, tree, config, title, title1, title2):
        '''
        Tags on UC has two mode, directly shown on the webpage or need to click the page first then show the
        detail info. This function will handle the first kind of tag, scrapping the tags' name and weight, saving
        the final result into a dict {name: weight}

        :param tree: XML object
        :param config: config from config variable
        :param title:  first layer of the tag components
        :param title1: second layer of the tag components
        :param title2: third layer of the tag components
        :return: tag dict {name: weight}
        '''

        tags = {}
        projectTags = tree.xpath(config.get(title))
        if len(projectTags) == 0: return {}
        name = projectTags[0].xpath(config.get(title1))
        weight = projectTags[0].xpath(config.get(title2))
        for i in range(len(name)):
            tags.update({name[i]: weight[i]})
        return tags

    def getTags(self, tree, config, title, title1, title2, title3):
        '''
        This function will handling the second type of tags, saving the final result into a dict {name: weight}

        :param tree: XML object
        :param config: config from config variable
        :param title:  first layer of the tag components
        :param title1: second layer of the tag components
        :param title2: third layer of the tag components
        :param title3: forth layer of the tag components
        :return: tag dict {name: weight}
        '''
        urlHead = 'https://researchprofiles.canberra.edu.au'
        fingerPrintUrl = tree.xpath(config.get(title))
        Url = ''
        for i in fingerPrintUrl:
            if title1 in i:
                Url = i
        if Url == '' or len(fingerPrintUrl) == 0:
            return None
        fingerPrint = requests.get(urlHead + Url, headers=self.headers, proxies=self.proxy)
        fingerPrint = fingerPrint.text
        fingerPrint = etree.HTML(fingerPrint)
        tags = fingerPrint.xpath(config.get(title2))
        weights = fingerPrint.xpath(config.get(title3))
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

    def save2Mongo(self):
        '''
        :return: True if successfully saved, otherwise False
        '''
        host = cfg.mongo_host
        port = cfg.mongo_port
        db = cfg.database_name
        user = cfg.username
        pwd = cfg.passwd
        today = date.today()
        t = today.strftime("%m_%d_%Y")
        collection = cfg.collection_name + '_' + t
        mongodb = mongo(host, port, user, pwd, db, collection)
        print(mongodb)  # baseinfo

        result = mongodb.insert(self.staffs)
        print(result.inserted_ids)
        print(len(mongodb))
        print(mongodb.find_all())
