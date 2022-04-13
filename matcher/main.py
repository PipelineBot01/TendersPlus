from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
# from researcher.update.researcher_updater import ResearcherUpdater
# from tenders.update.tenders_updater import TendersUpdater
from datetime import datetime, timedelta



def fn():
    print(f'{datetime.now()} -- start update')
    #
    # ru = ResearcherUpdater()
    # ru.update()
    #
    # tu = TendersUpdater()
    # tu.update()
    #
    # print(f'{datetime.now()} -- done update')



if __name__ == '__main__':
    bs = BlockingScheduler(daemon=True)
    bs.add_job(fn, 'interval',seconds=1)
    try:
        bs.start()
    except Exception as e:
        bs.shutdown()
