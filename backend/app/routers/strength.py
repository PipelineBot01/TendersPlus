from fastapi import APIRouter, HTTPException

from utils.matcher.utils.tool import get_research_strength

router = APIRouter()


@router.get('')
def get_strength_overview():
    try:
        data = get_research_strength()
        print(data,11111)
        return {'code': 200, 'data': data}
    except Exception as e:
        print(e)
        raise HTTPException(500, 'INTERNAL SERVER ERROR')
