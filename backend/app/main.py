from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError, HTTPException

from errors import validation_exception_handler
from errors import http_exception_handler

from router import tenders_router
from router import subscribe_router

from config import settings
from scheduler import async_scheduler
from db import init_db

# init app
server = FastAPI()

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

# setup router
server.include_router(tenders_router, prefix='/tenders', tags='Tenders')
server.include_router(subscribe_router, prefix='/subscribe', tags='Subscribe')


# setup startup event

@server.on_event('startup')
async def startup():
    init_db()
    # ====== init scheduler ======
    # run jobs
    for j in async_scheduler.jobs:
        if j['delay'] is False:
            await j['func']()

    async_scheduler.start()


# setup shutdown event
@server.on_event('shutdown')
async def shutdown():
    async_scheduler.shutdown(wait=True)


if __name__ == '__main__':
    import uvicorn

    # launch app
    if type(settings.APP_PORT) == 'str':
        port = int(settings.APP_PORT)
    else:
        port = settings.APP_PORT

    uvicorn.run(app=server, port=port, host=settings.APP_HOST)
