from apscheduler.schedulers.blocking import BlockingScheduler

from researcher.update.researcher_updater import ResearcherUpdater
from tenders.update.tenders_updater import TendersUpdater
from datetime import datetime



def fn():
    print(f'{datetime.now()} -- start update')

    ru = ResearcherUpdater()
    ru.update()

    tu = TendersUpdater()
    tu.update()

    print(f'{datetime.now()} -- done update')



if __name__ == '__main__':
    bs = BlockingScheduler(daemon=True)
    bs.add_job(fn, 'interval',seconds=5)
    try:
        bs.start()
    except Exception as e:
        bs.shutdown()
