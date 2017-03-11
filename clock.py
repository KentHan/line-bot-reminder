from apscheduler.schedulers.blocking import BlockingScheduler


sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=5)
def scheduled_job():
    print('This job is run every five seconds.')

sched.start()