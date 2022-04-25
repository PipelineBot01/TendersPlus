import requests
import json
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get('')
def get_strength_overview():
    try:
        data = {}
        response = requests.get('http://localhost:20222/get_university_strength')
        if response.status_code == 200:
            data = json.loads(response.content)['data']
        return {'code': 200, 'data': data}
    except Exception as e:
        print(e)

        raise HTTPException(500, 'INTERNAL SERVER ERROR')
