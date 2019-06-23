# -*- coding: utf-8 -*-

import os
import logging

from apscheduler.schedulers.blocking import BlockingScheduler

from bo import EventBO

bo = EventBO()

# sched = BlockingScheduler()
# @sched.scheduled_job('cron', minute="*")
# def scheduled_job():
# 	bo.send_notification()
# sched.start()

bo.send_notification()