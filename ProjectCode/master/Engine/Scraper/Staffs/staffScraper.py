"""
The skeleton of staff scrapper, control the process of scrapping. Detail plug tool can be called by changing the config
when scrapping different universities.

Authors:
- Leyang Chai u7201445
"""


from supportUni import uni
from config.UC.UC_plug import UC_plug


class staffScraper():
    def __init__(self, interval, saveInfo=['tempResult\\ScraperResult_UC', '.csv'], config='UC', proxies = None):
        '''

        :param interval: time interval between visiting each link
        :param saveInfo: location for saving local file, do not save local file if this attribute is None
        :param config: name for the config tool
        :param proxies: proxy for scrapper, only using for vpn
        '''
        self.interval = interval
        self.saveInfo = saveInfo

        # setting socks5 proxy
        self.proxy = proxies
        self.config = config
        self.scrapper_tool = None

    def loadConfig(self):
        '''
        load configuration file and ini the scrapper tool to the required one. The supported tools should be contained
        in supportUni.py, otherwise will raise error
        '''

        print('Loading config file')
        assert (uni.keys().__contains__(self.config)), 'current program only support '+', '.join(uni.values())
        if self.config == 'UC': self.scrapper_tool = UC_plug(self.interval, self.saveInfo, self.proxy)


    def run(self):
        '''

        :return:
        '''
        print('Asking url')
        self.scrapper_tool.getLinks()
        print('Scrap user info')
        self.scrapper_tool.getUserInfo()
        print('Saving to MongoDB')
        self.scrapper_tool.save2Mongo()
