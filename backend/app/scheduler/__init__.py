"""
The scheduler do the following things:
1. update the latest, hot, and expiring soon opportunities
2. update the relationship with tenders and tags
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .jobs import jobs

# 1. create engine
async_scheduler = AsyncIOScheduler()

# 2. add jobs
for j in jobs:
    async_scheduler.add_job(**j)

# 3. store all jobs func
async_scheduler.__setattr__('jobs', jobs)
