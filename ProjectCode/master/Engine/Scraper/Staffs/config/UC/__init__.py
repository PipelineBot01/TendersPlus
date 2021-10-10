from Staff import Staff
import sys
sys.path.append("..")
from MongoDB import cfg
from MongoDB.mongoDB import mongo

config = {
    'url': 'https://researchprofiles.canberra.edu.au/en/persons/',
    'urlHead': 'https://researchprofiles.canberra.edu.au/en/persons/?format=&page=',
    'pageNav': '//nav[@class="pages"]/ul/li/a/text()',
    'staffUrl': '//a[@rel="Person"]/@href',
    'staffName': '//a[@rel="Person"]/span/text()',
    'Email': '//li[@class="emails"]/span/a/@href',
    'Title': '//span[@class="job-title"]/text()',
    'Organisation': '//a[@rel="Organisation"]/span/text()',
    'Details': '//a[@class="portal_link btn-primary btn-large"]/@href',
    'Tag': '//span[@class="concept"]/text()',
    'TagWeight': '//span[@class="value sr-only"]/text()',
    'Profile': '//div[@class="textblock"]',
    'FingerPrintSection': '//section[@class="page-section content-relation-section person-fingerprint"]/div/ul/li/button/span/span',
    'ProjectSection': '//div[@class="relation-list relation-list-publications"]/ul/li/div/ul/li/button/span/span'
}