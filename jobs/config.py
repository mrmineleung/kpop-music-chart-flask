import os

from apscheduler.jobstores.mongodb import MongoDBJobStore
from flask_pymongo import MongoClient

client = MongoClient(os.environ.get('MONGO_URI'))
class Config:
    DEBUG = True
    SCHEDULER_API_ENABLED = True
    SCHEDULER_JOBSTORES = {
        'default': MongoDBJobStore(client=client)
    }
    SCHEDULER_TIMEZONE = 'America/Atikokan'
