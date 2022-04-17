from tenders.update_go import update_go

from apscheduler.schedulers.blocking import BlockingScheduler

from datetime import datetime


def fn():
    if datetime.now().hour < 3:
        update_go()


if __name__ == '__main__':
    fn()
    bs = BlockingScheduler(daemon=True)
    bs.add_job(fn, 'interval', hours=1)
    try:
        bs.start()
    except Exception as e:
        bs.shutdown()
