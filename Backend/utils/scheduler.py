# utils/scheduler.py

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from datetime import datetime
import asyncio
import logging

from Backend.controllers.batch_review_controller import batch_update_review_scores
from Backend.controllers.batch_seller_controller import batch_update_seller_scores

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

# listener to log and chain jobs
def job_listener(event):
    if event.exception:
        logger.error(f"❌ Job {event.job_id} failed at {datetime.now()}: {event.exception}")
    else:
        logger.info(f"✅ Job {event.job_id} executed at {datetime.now()}")
        # as soon as reviews are scored, kickoff seller scoring
        if event.job_id == "daily_review_score_update":
            # schedule it immediately in the event loop
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    loop.create_task(batch_update_seller_scores())
                else:
                    logger.warning("Event loop not running, cannot chain seller scoring")
            except RuntimeError:
                logger.warning("No event loop available, cannot chain seller scoring")

scheduler.add_listener(
    job_listener,
    EVENT_JOB_EXECUTED | EVENT_JOB_ERROR
)

# schedule review‐scoring every day at 2am (or every minute for testing)
review_job = scheduler.add_job(
    batch_update_review_scores,
    trigger=CronTrigger(minute="*/4"),#hour=2, minute=0
    id="daily_review_score_update",
    replace_existing=True
)
logger.info(f"Scheduled review‐scoring job with id '{review_job.id}'")

def start_scheduler():
    if not scheduler.running:
        try:
            scheduler.start()
            logger.info("Scheduler started with jobs: %s", [j.id for j in scheduler.get_jobs()])
        except RuntimeError as e:
            logger.warning(f"Scheduler could not start immediately: {e}")
            logger.info("Scheduler will start when event loop is available")

def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler shut down")
