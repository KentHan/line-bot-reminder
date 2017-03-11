# -*- coding: utf-8 -*-

import os

from apscheduler.schedulers.blocking import BlockingScheduler

from pymongo import MongoClient

mongodb_id = os.getenv('MONGODB_ID')
mongodb_pw = os.getenv('MONGODB_PW')

client = MongoClient("mongodb://cluster1-shard-00-00-imdfs.mongodb.net:27017,cluster1-shard-00-01-imdfs.mongodb.net:27017,cluster1-shard-00-02-imdfs.mongodb.net:27017/admin?ssl=true&replicaSet=Cluster1-shard-0&authSource=admin")
client.admin.authenticate(mongodb_id, mongodb_pw, mechanism='SCRAM-SHA-1')
db = client.user_data

sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=5)
def scheduled_job():
    print('This job is run every five seconds.')
    query = db["users"].find()
    print("DB count: %d" % query.count())

sched.start()