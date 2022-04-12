from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

bs = BlockingScheduler()

def fn():

    pass


bs.add_job(fn, IntervalTrigger(hours=1, timezone='Asia/Hong_Kong'))
bs.start()
