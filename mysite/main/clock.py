import time
import os
import datetime
import schedule
from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def cr():
    print('do crawler') 
    os.system("python main/imdbCrawl.py") 


sched.start()