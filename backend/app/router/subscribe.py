from fastapi import APIRouter
from models import SubscribeModel

router = APIRouter()


@router.post('')
def subscribe(data: SubscribeModel):
    return {'code': 0, 'data': 'subscribe'}
