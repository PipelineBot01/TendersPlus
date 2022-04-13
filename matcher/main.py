from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
# from researcher.update.researcher_updater import ResearcherUpdater
# from tenders.update.tenders_updater import TendersUpdater
# from datetime import datetime, timedelta
# import requests


def fn():
    print('aaa')
    # print(f'{datetime.now()} -- start update')
    #
    # ru = ResearcherUpdater()
    # ru.update()
    #
    # tu = TendersUpdater()
    # tu.update()
    #
    # print(f'{datetime.now()} -- done update')



if __name__ == '__main__':
    bs = BlockingScheduler(executors={
        'default':ThreadPoolExecutor(5)
    },daemon=True)
    bs.add_job(fn, IntervalTrigger(seconds=10, timezone='Asia/Hong_Kong'))
    try:
        bs.start()
    except Exception as e:
        bs.shutdown()
