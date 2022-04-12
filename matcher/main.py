from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from researcher.update.researcher_updater import ResearcherUpdater
from tenders.update.tenders_updater import TendersUpdater

bs = BlockingScheduler()


def fn():
    ru = ResearcherUpdater()
    ru.update()

    tu = TendersUpdater()
    tu.update()


bs.add_job(fn, IntervalTrigger(seconds=10, timezone='Asia/Hong_Kong'))
bs.start()