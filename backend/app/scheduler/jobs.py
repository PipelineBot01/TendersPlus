from apscheduler.triggers.base import BaseTrigger
from apscheduler.triggers.interval import IntervalTrigger

jobs = []


def job(id: str, trigger: BaseTrigger, delay: bool = False):
    def decorator(fn):
        jobs.append({'id': id, 'trigger': trigger, 'func': fn, 'delay': delay})
        return fn

    return decorator


@job(id='crawl_data', trigger=IntervalTrigger(minutes=1, timezone='Asia/Hong_Kong'), delay=True)
async def get_tenders():
    pass
    # url="https://www.tenders.gov.au/Atm/"
    # interval=3
    # scraper=tenderScraper(url, interval)
    # scraper.run(save_mongo=True)


@job(id='update_latest_tenders', trigger=IntervalTrigger(minutes=1, timezone='Asia/Hong_Kong'))
async def update_latest_tenders():
    # print('scheduled job: update_latest_tenders Done!')
    pass

@job(id='update_expiring_tenders', trigger=IntervalTrigger(hours=1, timezone='Asia/Hong_Kong'))
async def update_expiring_tenders():
    # TODO: filter out tenders that expiring within one month, and save to the mongodb
    pass


@job(id='update_hot_tenders', trigger=IntervalTrigger(hours=1, timezone='Asia/Hong_Kong'))
async def update_hot_tenders():
    # TODO: rearrange tenders rank based on user interactions.
    pass
