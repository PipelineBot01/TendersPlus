"""
Before run the test, make sure the .env file is in current folder
"""

import json
import random

from faker import Faker
from locust import HttpUser, task, between
from locust.env import Environment
from locust.log import setup_logging

from config import settings

faker = Faker()

research_field_keys = [k for k, v in settings.RESEARCH_FIELDS.items()]


class SimulateClient(HttpUser):
    wait_time = between(1, 2)
    host = 'http://localhost:20220'

    @task
    def api_test(self):
        """
        Use "faker" to generate many users, with different email, first name, last name, university and research fields
        email: EmailStr
        first_name: str
        last_name: str
        university: str
        password: str
        confirmed_password: str
        research_fields: List[str]
        """
        for i in range(10):

            # generate a fake user
            user = {'email': faker.email(),
                    'first_name': faker.first_name(),
                    'last_name': faker.last_name(),
                    'university': random.choice(settings.UNIVERSITIES),
                    'research_fields': set(),
                    'password': faker.password()}
            user['confirmed_password'] = user['password']
            for j in range(random.randint(1, 3)):
                user['research_fields'].add(random.choice(research_field_keys))
            user['research_fields'] = list(user['research_fields'])
            # simulate 'signup' action
            with self.client.post(url='/account/signup',
                                  json=user,
                                  catch_response=True) as signup_response:
                code = signup_response.status_code

                try:
                    content = json.loads(signup_response.content)
                except:
                    content = {}

                if code == 200:
                    res = content['data']
                    user['access_token'] = res['access_token']

                    with self.client.post(url='/account/login',
                                          json={'email': user['email'],
                                                'password': user['password']},
                                          catch_response=True) as login_response:
                        if login_response.status_code == 200:
                            login_response.success()
                        else:
                            login_response.failure('Failed ')
                else:
                    print(content)
                    if 'msg' in content:
                        signup_response.failure(content['msg'])
                    else:
                        signup_response.failure('Unknown error')


setup_logging("INFO", None)

# setup Environment and Runner
env = Environment(user_classes=[SimulateClient])
env.create_local_runner()

# start a WebUI instance
env.create_web_ui("localhost", 8089)
env.runner.greenlet.join()
