
mongo_host = '110.40.137.110'
mongo_port = '27017'
username = 'tenderplus'
passwd = 'tenderPlus@2021'
database_name = 'tenders'

go_config = (mongo_host, mongo_port, username, passwd, database_name, 'raw_grants_opened')
seed_url = 'https://www.grants.gov.au/go/list'
url_head = 'https://www.grants.gov.au/go/list'
go_head = "https://www.grants.gov.au"
parser_config = {
            'Title': '//*[@role="heading"]/text()',
            'labels': '//*[@id="mainContent"]/div/div[2]/div[2]/div[1]//*[@class = "list-desc"]/span/text()',
            'Details': '//*[@id="mainContent"]/div/div[2]/div[2]/div[1]//*/text()'
        }
interval = 1
SAVE_MONGO = True