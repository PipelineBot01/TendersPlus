from datetime import datetime
import time

from go_conf import go_config, seed_url, url_head, go_head, parser_config, interval, SAVE_MONGO
from engine.httpScraper import goScraper
from .update_raw import update_raw_all


def update_go():

    UPDATE = False
    print("*********** start update raw_grant_opened **********")
    print(f'{datetime.now()} -- start update')
    go_update = goScraper(config=go_config, seed_url=seed_url, url_head=url_head, go_head=go_head,
                          parser_config=parser_config, interval=interval, save_mongo=SAVE_MONGO)
    # At most 5 attempts to scrape data
    try_limits = 5
    while True:
        print("remaining attempts: {}, start time {}".format(try_limits,datetime.now()))
        try_limits = try_limits - 1
        go_update.run()
        if go_update.get_scrape_complete():
            UPDATE = True
            break
        # run out of attempts
        if try_limits < 0:
            print("run out of attempts")
            break
        # sleep 2 min then reattempt to scrape

        time.sleep(120)

    if UPDATE:
        print(f'{datetime.now()} -- done update')

        print("*********** start update raw_grant_all **********")
        print(f'{datetime.now()} -- start update')
        update_raw_all()

        print(f'{datetime.now()} -- done update')
    else:
        print(f'{datetime.now()} -- update fail')


