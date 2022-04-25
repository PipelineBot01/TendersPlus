from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
#
from researcher.update.researcher_updater import ResearcherUpdater
from tenders.update.tenders_updater import TendersUpdater
from auto_reco import tenders_filter
from researcher.matching import researcher_matcher

scheduler = AsyncIOScheduler()


@scheduler.scheduled_job(id='update_tenders_pool', trigger=IntervalTrigger(hours=2))
async def update_tenders_pool():
    if 2 < datetime.now().hour < 6:
        print(datetime.now().strftime(fmt='%Y-%m-%d %H:%M:%S') + ' ------ start update tenders pool')
        TendersUpdater().update()
        tenders_filter.update_data()
        print(datetime.now().strftime(fmt='%Y-%m-%d %H:%M:%S') + ' ------ end update tenders pool')


@scheduler.scheduled_job(id='update_researchers_pool', trigger=IntervalTrigger(hours=1))
async def update_researchers_pool():
    if 20 < datetime.now().hour < 8:
        print(datetime.now().strftime(fmt='%Y-%m-%d %H:%M:%S') + ' ------ start update researchers pool')
        ResearcherUpdater().update()
        tenders_filter.update_data()
        researcher_matcher.update()
        print(datetime.now().strftime(fmt='%Y-%m-%d %H:%M:%S') + ' ------ end update researchers pool')
