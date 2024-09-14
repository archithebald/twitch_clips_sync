from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from database import every_month

scheduler = BlockingScheduler()

scheduler.add_job(every_month, trigger=CronTrigger(day=1, hour=10, minute=0))

scheduler.start()