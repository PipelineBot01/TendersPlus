from pydantic import BaseModel
from typing import Optional, List
from fastapi import FastAPI

from scheduler import scheduler
from filter.filter import Filter
from researcher.matching.researcher_relation import ResearcherMatcher
from utils.tool_utils import get_research_strength

# create web server
app = FastAPI()


# define api parameters
class Profile(BaseModel):
    id: Optional[str]
    divisions: List[str]
    tags: List[str]


@app.post('/get_sim_researchers')
async def get_sim_researchers(data: Profile):
    return {'code': 200, 'data': ResearcherMatcher().match_by_profile(data)}


@app.post('/get_reco_tenders')
async def get_reco_tenders(data: Profile):
    return {'code': 200, 'data': Filter().match(data)}


@app.get('/get_research_strength')
async def get_research_strength():
    return {'code': 200, 'data': get_research_strength()}


@app.on_event('startup')
async def init():
    print('initial update task')
    job_1 = scheduler.get_job(job_id='update_tenders_pool')
    if job_1:
        await job_1.func()

    job_2 = scheduler.get_job(job_id='update_researchers_pool')
    if job_2:
        await job_2.func()

    scheduler.start()


@app.on_event('shutdown')
async def close():
    scheduler.shutdown()


if __name__ == '__main__':
    import uvicorn
    from uvicorn.config import LOGGING_CONFIG

    # modify log
    log_config = LOGGING_CONFIG.copy()
    log_config['formatters']['default']['fmt'] = '%(asctime)s    ' + log_config['formatters']['default']['fmt']
    log_config['formatters']['access']['fmt'] = '%(asctime)s    ' + log_config['formatters']['access']['fmt']

    # launch app
    uvicorn.run(app=app, port=20222, host='localhost', log_config=log_config)
