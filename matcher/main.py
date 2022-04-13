from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from researcher.update.researcher_updater import ResearcherUpdater
from tenders.update.tenders_updater import TendersUpdater
from datetime import datetime, timedelta




def fn():
    print(f'{datetime.now()} -- start updating')

    ru = ResearcherUpdater()
    ru.update()

    tu = TendersUpdater()
    tu.update()

bs = BlockingScheduler()
bs.add_job(fn, IntervalTrigger(hours=1, timezone='Asia/Hong_Kong'), next_run_time=datetime.now()+timedelta(seconds=5))
bs.start()
