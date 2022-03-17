from fastapi import APIRouter
from typing import Union, Optional

router = APIRouter()


@router.get('/latest')
def get_latest_tenders(n: Optional[Union[str, int]]):
    # TODO get_latest_tenders
    return {'code': 0, 'data': 'get_latest_tenders'}


@router.get('/hot')
def get_hot_tenders(n: Optional[Union[str, int]]):
    # TODO get_hot_tenders
    return {'code': 0, 'data': 'get_hot_tenders'}


@router.get('/expiring')
def get_expiring_soon_tenders(n: Optional[Union[str, int]]):
    # TODO get_expiring_soon_tenders
    return {'code': 0, 'data': 'get_expiring_soon_tenders'}


@router.get('')
def get_tags_tenders(tags: str):
    # TODO get_tags_tenders
    return {'code': 0, 'data': 'get_tags_tenders'}
