# utils/scheduler.py

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from datetime import datetime
import asyncio

from Backend.controllers.batch_review_controller import batch_update_review_scores
from Backend.controllers.batch_seller_controller import batch_update_seller_scores

scheduler = AsyncIOScheduler()

# listener to log and chain jobs
def job_listener(event):
    if event.exception:
        print(f"❌ Job {event.job_id} failed at {datetime.now()}")
    else:
        print(f"✅ Job {event.job_id} executed at {datetime.now()}")
        # as soon as reviews are scored, kickoff seller scoring
        if event.job_id == "daily_review_score_update":
            # schedule it immediately in the event loop
            asyncio.get_event_loop().create_task(batch_update_seller_scores())

scheduler.add_listener(
    job_listener,
    EVENT_JOB_EXECUTED | EVENT_JOB_ERROR
)

# schedule review‐scoring every day at 2am (or every minute for testing)
review_job = scheduler.add_job(
    batch_update_review_scores,
    trigger=CronTrigger(minute="*/30"),#hour=2, minute=0
    id="daily_review_score_update",
    replace_existing=True
)
print(f"Scheduled review‐scoring job with id '{review_job.id}'")

def start_scheduler():
    if not scheduler.running:
        scheduler.start()
        print("Scheduler started with jobs:", [j.id for j in scheduler.get_jobs()])

def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        print("Scheduler shut down")
