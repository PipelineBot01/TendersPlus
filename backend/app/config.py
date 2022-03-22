from pydantic import BaseSettings
from typing import List
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--env_path', type=str, action='store')
env_path = parser.parse_args().env_path

if env_path is None:
    env_path = './.env'


class Settings(BaseSettings):
    # nosql server
    MONGO_URL: str
    MONGO_USERNAME: str
    MONGO_PASSWORD: str

    # mysql server
    MYSQL_USERNAME: str
    MYSQL_PASSWORD: str
    MYSQL_URL: str
    MYSQL_DATABASE: str

    # use to filter out tenders
    EXPIRING_WEEK_THRESHOLD: int = 1
    LATEST_WEEK_THRESHOLD: int = 8
    HOT_THRESHOLD: str = ''

    # app server
    APP_HOST: str = 'localhost'
    APP_PORT: int = 202202
    DATETIME_FORMAT = '%d-%b-%Y'

    LATEST_OPPORTUNITIES: dict = None
    HOT_OPPORTUNITIES: dict = None

    OAUTH_SECRET_KEY: str
    UNIVERSITIES = ['Australian National University', 'University of Canberra', 'Australian Catholic University',
                    'Charles Sturt University', 'Macquarie University', 'Southern Cross University',
                    'University of New England', 'University of New South Wales', 'University of Newcastle',
                    'University of Sydney', 'University of Technology, Sydney', 'Western Sydney University',
                    'University of Wollongong', 'Charles Darwin University',
                    'Bond University', 'CQ University', 'Federation University of Australia', 'Griffith University',
                    'James Cook University', 'Queensland University of Technology', 'University of Queensland',
                    'University of Southern Queensland', 'University of the Sunshine Coast',
                    'Carnegie Mellon University', 'Flinders University', 'Torrens University Australia',
                    'University of Adelaide', 'University of South Australia', 'University of Tasmania',
                    'Deakin University', 'Federation University of Australia', 'La Trobe University',
                    'Monash University', 'RMIT University', 'Swinburne University of Technology',
                    'University of Divinity', 'University of Melbourne', 'Victoria University',
                    'Curtin University', 'Edith Cowan University', 'Murdoch University',
                    'University of Notre Dame Australia', 'University of Western Australia'
                    ]
    RESEARCH_FIELDS = ['MATHEMATICAL', 'PHYSICAL', 'CHEMICAL', 'EARTH'
        , 'ENVIRONMENTAL', 'BIOLOGICAL', 'AGRICULTURAL AND VETERINARY', 'INFORMATION AND COMPUTINGs',
                       'ENGINEERING', 'TECHNOLOGY', 'MEDICAL AND HEALTH', 'BUILT ENVIRONMENT AND DESIGN',
                       'EDUCATION', 'ECONOMICS', 'COMMERCE, MANAGEMENT, TOURISM AND SERVICES',
                       'STUDIES IN HUMAN SOCIETY',
                       'PSYCHOLOGY AND COGNITIVE SCIENCES', 'LAW AND LEGAL STUDIES',
                       'STUDIES IN CREATIVE ARTS AND WRITING',
                       'LANGUAGE, COMMUNICATION AND CULTURE', 'HISTORY AND ARCHAEOLOGY',
                       'PHILOSOPHY AND RELIGIOUS STUDIES'
                       ]


settings = Settings(_env_file=env_path)
