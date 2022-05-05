"""
Before run the test, make sure the .env file is in current folder
"""
import base64
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
        keyword = ''
        for j in range(random.randint(1, 5)):
            keyword += faker.word()+' '
        keyword = base64.b64encode(keyword.encode("utf-8")).decode('utf-8')
        with self.client.get(url=f'/search?query={keyword}&n=3',
                              catch_response=True) as search_response:

            if search_response.status_code == 200:
                search_response.success()
            else:
                search_response.failure(search_response.content)


setup_logging("INFO", None)

# setup Environment and Runner
env = Environment(user_classes=[SimulateClient])
env.create_local_runner()

# start a WebUI instance
env.create_web_ui("localhost", 8089)
env.runner.greenlet.join()
