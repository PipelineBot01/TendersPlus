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

    APP_PORT: int = 20220

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
                    'Deakin University', 'La Trobe University',
                    'Monash University', 'RMIT University', 'Swinburne University of Technology',
                    'University of Divinity', 'University of Melbourne', 'Victoria University',
                    'Curtin University', 'Edith Cowan University', 'Murdoch University',
                    'University of Notre Dame Australia', 'University of Western Australia'
                    ]
    RESEARCH_FIELDS = {
        'd_01': {
            'field': 'MATHEMATICAL',
            'sub_fields': ['Pure Mathematics',
                           'Applied Mathematics',
                           'Numerical and Computational Mathematics',
                           'Statistics',
                           'Mathematical Physics',
                           'Other Mathematical']
        },
        'd_02': {
            'field': 'PHYSICAL',
            'sub_fields': ['Astronomical and Space Sciences',
                           'Atomic, Molecular, Nuclear, Particle and Plasma Physics',
                           'Classical Physics',
                           'Condensed Matter Physics',
                           'Optical Physics',
                           'Quantum Physics',
                           'Other Physics']
        },
        'd_03': {
            'field': 'CHEMICAL',
            'sub_fields': []
        },
        'd_04': {
            'field': 'EARTH',
            'sub_fields': []
        },
        'd_05': {
            'field': 'ENVIRONMENTAL',
            'sub_fields': []
        },
        'd_06': {
            'field': 'BIOLOGICAL',
            'sub_fields': []
        },
        'd_07': {
            'field': 'AGRICULTURAL AND VETERINARY',
            'sub_fields': []
        },
        'd_08': {
            'field': 'INFORMATION AND COMPUTINGs',
            'sub_fields': []
        },
        'd_09': {
            'field': 'ENGINEERING',
            'sub_fields': []
        },
        'd_10': {
            'field': 'TECHNOLOGY',
            'sub_fields': []
        },
        'd_11': {
            'field': 'MEDICAL AND HEALTH',
            'sub_fields': []
        },
        'd_12': {
            'field': 'BUILT ENVIRONMENT AND DESIGN',
            'sub_fields': []
        },
        'd_13': {
            'field': 'EDUCATION',
            'sub_fields': []
        },
        'd_14': {
            'field': 'ECONOMICS',
            'sub_fields': []
        },
        'd_15': {
            'field': 'COMMERCE, MANAGEMENT, TOURISM AND SERVICES',
            'sub_fields': []
        },
        'd_16': {
            'field': 'STUDIES IN HUMAN SOCIETY',
            'sub_fields': []
        },
        'd_17': {
            'field': 'PSYCHOLOGY AND COGNITIVE SCIENCES',
            'sub_fields': []
        },
        'd_18': {
            'field': 'LAW AND LEGAL STUDIES',
            'sub_fields': []
        },
        'd_19': {
            'field': 'STUDIES IN CREATIVE ARTS AND WRITING',
            'sub_fields': []
        },
        'd_20': {
            'field': 'LANGUAGE, COMMUNICATION AND CULTURE',
            'sub_fields': []
        },
        'd_21': {
            'field': 'HISTORY AND ARCHAEOLOGY',
            'sub_fields': []
        },
        'd_22': {
            'field': 'PHILOSOPHY AND RELIGIOUS STUDIES',
            'sub_fields': []
        }
    }


settings = Settings(_env_file=env_path)
