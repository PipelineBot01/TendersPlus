from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError, HTTPException

from errors import validation_exception_handler
from errors import http_exception_handler

from routers import account_router, user_router, matcher_router,strength_router

from config import settings
from scheduler import async_scheduler
from db.mysql import init_db as init_mysql

# init app
server = FastAPI(root_path='/tendersplus/api')

# setup middleware
server.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# setup HTTP exception handler
server.add_exception_handler(RequestValidationError, validation_exception_handler)
server.add_exception_handler(HTTPException, http_exception_handler)

# setup routers
server.include_router(account_router, prefix='/account', tags=['Account'])
server.include_router(user_router, prefix='/user', tags=['User'])
server.include_router(matcher_router, prefix='/matcher', tags=['Matcher'])
server.include_router(strength_router, prefix='/strength_overview', tags=['StrengthOverview'])


# setup startup event
@server.on_event('startup')
async def startup():
    init_mysql()
    # ====== init scheduler ======
    # run jobs
    for j in async_scheduler.jobs:
        if j['delay'] is False:
            await j['func']()

    # async_scheduler.start()


# setup shutdown event
@server.on_event('shutdown')
async def shutdown():
    async_scheduler.shutdown(wait=True)


if __name__ == '__main__':
    import uvicorn

    # launch app
    uvicorn.run(app=server, port=int(settings.APP_PORT), host=settings.APP_HOST, root_path='/tendersplus/api')
