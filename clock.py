# -*- coding: utf-8 -*-

import os
import logging

from apscheduler.schedulers.blocking import BlockingScheduler

from pymongo import MongoClient

from message import send_text_message

mongodb_id = os.getenv("MONGODB_ID")
mongodb_pw = os.getenv("MONGODB_PW")
mongodb_uri = os.getenv("MONGODB_URI")

client = MongoClient(mongodb_uri)
client.admin.authenticate(mongodb_id, mongodb_pw, mechanism='SCRAM-SHA-1')
db = client.user_data

logging.basicConfig()

sched = BlockingScheduler()

@sched.scheduled_job('cron', minute="*")
def scheduled_job():
    print('This job is run every five seconds.')
    query = db["users"].find()
    print("DB count: %d" % query.count())
    send_text_message("U171903a51154a9693c8c49fbce6af0d1", "我想吃藥了！")
    print('This job is finished.')

sched.start()
