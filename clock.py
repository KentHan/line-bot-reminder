# -*- coding: utf-8 -*-

import os
import logging

from apscheduler.schedulers.blocking import BlockingScheduler

from pymongo import MongoClient

from linebot import LineBotApi
from linebot.models import TextMessage

channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
line_bot_api = LineBotApi(channel_access_token)

mongodb_id = os.getenv("MONGODB_ID")
mongodb_pw = os.getenv("MONGODB_PW")
mongodb_uri = os.getenv("MONGODB_URI")

client = MongoClient(mongodb_uri)
client.admin.authenticate(mongodb_id, mongodb_pw, mechanism='SCRAM-SHA-1')
db = client.user_data

logging.basicConfig()

def sendTextMessage(user_id, text):
	message = TextMessage("1", text)
	line_bot_api.push_message(user_id, message)

sched = BlockingScheduler()

@sched.scheduled_job('cron', hour="8-24",minute="0")
def scheduled_job():
    print('This job is run every five seconds.')
    query = db["users"].find()
    print("DB count: %d" % query.count())
    sendTextMessage("U171903a51154a9693c8c49fbce6af0d1", "我想吃藥了！")
    print('This job is finished.')

sched.start()
