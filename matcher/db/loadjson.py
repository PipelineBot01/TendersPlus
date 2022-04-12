import json
import pandas as pd
import requests
from db_conf import JSON_URL_USER, JSON_URL_ACT


def get_data(data_name='user') -> pd.DataFrame:
    assert data_name in ['user', 'action'], 'dataset not find'
    url = JSON_URL_USER if data_name == 'user' else JSON_URL_ACT
    response = requests.get(url, headers={'X-TOKEN': '%Ef0-b2jv[3;]]`1`*124cvBsp[lAsc;'})
    return pd.DataFrame(json.loads(response.content)['data'])
