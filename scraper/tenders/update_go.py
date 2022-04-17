from datetime import datetime

from go_conf import go_config, seed_url, url_head, go_head, parser_config, interval, SAVE_MONGO
from engine.httpScraper import goScraper
from update_raw import update_raw_all


def update_go():
    print("*********** start update raw_grant_opened **********")
    print(f'{datetime.now()} -- start update')
    go_update = goScraper(config=go_config, seed_url=seed_url, url_head=url_head, go_head=go_head,
                          parser_config=parser_config, interval=interval, save_mongo=SAVE_MONGO)
    go_update.run()

    print(f'{datetime.now()} -- done update')

    print("*********** start update raw_grant_all **********")
    print(f'{datetime.now()} -- start update')
    update_raw_all()

    print(f'{datetime.now()} -- done update')



