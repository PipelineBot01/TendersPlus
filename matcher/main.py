from fastapi import FastAPI
from apscheduler.schedulers.blocking import BlockingScheduler
# from researcher.update.researcher_updater import ResearcherUpdater
from tenders.update.tenders_updater import TendersUpdater
from datetime import datetime


def fn():
    print(f'{datetime.now()} -- start update')

    # ru = ResearcherUpdater()
    # ru.update()

    tu = TendersUpdater()
    tu.update()

    print(f'{datetime.now()} -- done update')


app = FastAPI()

app.on_event('startup')


if __name__ == '__main__':
    import uvicorn
    from uvicorn.config import LOGGING_CONFIG

    # modify log
    log_config = LOGGING_CONFIG.copy()
    log_config['formatters']['default']['fmt'] = '%(asctime)s    ' + log_config['formatters']['default']['fmt']
    log_config['formatters']['access']['fmt'] = '%(asctime)s    ' + log_config['formatters']['access']['fmt']

    # launch app
    uvicorn.run(app=app, port=20222, host='localhost', log_config=log_config)
