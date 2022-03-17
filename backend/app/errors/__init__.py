"""
Unify error response for all routes
"""
from fastapi import Request
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    msg = ''
    for error in exc.errors():
        if error.get('type') == 'value_error':
            msg = error.get("msg")
        else:
            if len(error.get("loc")) > 1:
                filed = error.get("loc")[1]
                msg = f"{filed}: {error.get('msg')}"
            else:
                msg = error.get("msg")
        break

    return JSONResponse(status_code=400, content={'code': 400, 'msg': msg})


# general http exception
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={'code': exc.status_code, 'msg': exc.detail})

