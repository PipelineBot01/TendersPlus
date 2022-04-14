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
    def __init__(self, config, seed_url, intervel, saveInfo=['results/historyInfo', '.csv']) -> None:
        self.config = config
        self.seed_url = seed_url
        self.saveInfo = saveInfo
        self.url_links = []
        host, port, user, pwd, db, collection = self.config
        self.db = mongo(host, port, user, pwd, db, collection)
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