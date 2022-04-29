from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
#
from researcher.update import ru
from tenders.update import tu
from auto_reco import reco_filter, reco_process
from researcher.matching import researcher_matcher
import time
scheduler = AsyncIOScheduler()


@scheduler.scheduled_job(id='update_tenders_pool', trigger=IntervalTrigger(hours=2))
async def update_tenders_pool():
    if 2 < datetime.now().hour < 6:
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' ------ start update tenders pool')
        tu.update()
        reco_filter.update()
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' ------ end update tenders pool')


@scheduler.scheduled_job(id='update_researchers_pool', trigger=IntervalTrigger(minutes=2))
async def update_researchers_pool():
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' ------ start update researchers pool')
    ru.update()
    researcher_matcher.update()
    reco_filter.update()
    reco_process.update()
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' ------ end update researchers pool')
