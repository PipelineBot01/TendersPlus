from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from researcher.update.researcher_updater import ResearcherUpdater
from tenders.update.tenders_updater import TendersUpdater
from datetime import datetime, timedelta
import requests


def fn():
    # print(f'{datetime.now()} -- start update')
    #
    # ru = ResearcherUpdater()
    # ru.update()
    #
    # tu = TendersUpdater()
    # tu.update()
    #
    # print(f'{datetime.now()} -- done update')
    print('requesting')
    requests.get('http://110.40.137.110/tendersplus/')


if __name__ == '__main__':
    fn()
    bs = BackgroundScheduler(daemon=True)
    bs.add_job(fn, IntervalTrigger(seconds=1, timezone='Asia/Hong_Kong'))
    try:
        bs.start()
        while True:
            pass
    except Exception as e:
        bs.shutdown()
