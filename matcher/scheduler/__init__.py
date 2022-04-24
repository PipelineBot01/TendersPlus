from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
#
# from researcher.update.researcher_updater import ResearcherUpdater
# from tenders.update.tenders_updater import TendersUpdater

scheduler = AsyncIOScheduler()
#
#
# @scheduler.scheduled_job(id='update_tenders_pool', trigger=IntervalTrigger(hours=2))
# async def update_tenders_pool():
#     if 2 < datetime.now().hour < 6:
#         print(datetime.now().strftime(fmt='%Y-%m-%d %H:%M:%S') + ' ------ start update tenders pool')
#         TendersUpdater().update()
#         print(datetime.now().strftime(fmt='%Y-%m-%d %H:%M:%S') + ' ------ end update tenders pool')
#
#
# @scheduler.scheduled_job(id='update_researchers_pool', trigger=IntervalTrigger(hours=1))
# async def update_researchers_pool():
#     if 20 < datetime.now().hour < 8:
#         print(datetime.now().strftime(fmt='%Y-%m-%d %H:%M:%S') + ' ------ start update researchers pool')
#         ResearcherUpdater().update()
#         print(datetime.now().strftime(fmt='%Y-%m-%d %H:%M:%S') + ' ------ end update researchers pool')

@scheduler.scheduled_job(id='test',trigger=IntervalTrigger(minutes=1))
def test():
    print('123')