from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from researcher.update.researcher_updater import ResearcherUpdater
from tenders.update.tenders_updater import TendersUpdater
from datetime import datetime, timedelta
import requests


def fn():
    print(f'{datetime.now()} -- start update')

    ru = ResearcherUpdater()
    ru.update()

    tu = TendersUpdater()
    tu.update()

    print(f'{datetime.now()} -- done update')



if __name__ == '__main__':
    fn()
    bg = BackgroundScheduler(daemon=True)
    bg.add_job(fn, IntervalTrigger(hours=1, timezone='Asia/Hong_Kong'))
    try:
        bg.start()
        while True:
            pass
    except Exception as e:
        bg.shutdown()
