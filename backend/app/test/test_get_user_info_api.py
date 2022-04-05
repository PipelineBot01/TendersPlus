import requests
import json


response = requests.get('http://110.40.137.110/tendersplus/api/user/all',headers={
    'X-TOKEN':'%Ef0-b2jv[3;]]`1`*124cvBsp[lAsc;'
})
print(json.loads(response.content))
