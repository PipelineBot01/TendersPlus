from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from researcher.update.researcher_updater import ResearcherUpdater
from tenders.update.tenders_updater import TendersUpdater
from datetime import datetime, timedelta


def fn():
    print(f'{datetime.now()} -- start update')

    ru = ResearcherUpdater()
    ru.update()

    tu = TendersUpdater()
    tu.update()

    print(f'{datetime.now()} -- done update')


fn()
bs = BackgroundScheduler()
bs.add_job(fn, IntervalTrigger(seconds=1, timezone='Asia/Hong_Kong'))
bs.start()
