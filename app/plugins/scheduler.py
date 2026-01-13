from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from typing import Callable, Dict, Any
import logging

logger = logging.getLogger(__name__)


class SchedulerPlugin:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.jobs: Dict[str, Dict[str, Any]] = {}
    
    async def start(self):
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("Scheduler started")
    
    async def stop(self):
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Scheduler stopped")
    
    def add_job(
        self,
        func: Callable,
        job_id: str,
        cron_expression: str,
        timezone: str = "UTC",
        **kwargs
    ):
        try:
            parts = cron_expression.split()
            if len(parts) != 5:
                raise ValueError("Invalid cron expression")
            
            minute, hour, day, month, day_of_week = parts
            
            trigger = CronTrigger(
                minute=minute,
                hour=hour,
                day=day,
                month=month,
                day_of_week=day_of_week,
                timezone=timezone
            )
            
            self.scheduler.add_job(
                func,
                trigger=trigger,
                id=job_id,
                **kwargs
            )
            
            self.jobs[job_id] = {
                "cron_expression": cron_expression,
                "timezone": timezone,
                "function": func.__name__
            }
            
            logger.info(f"Job {job_id} added with cron: {cron_expression}")
            return True
        except Exception as e:
            logger.error(f"Failed to add job {job_id}: {e}")
            return False
    
    def remove_job(self, job_id: str):
        try:
            self.scheduler.remove_job(job_id)
            if job_id in self.jobs:
                del self.jobs[job_id]
            logger.info(f"Job {job_id} removed")
            return True
        except Exception as e:
            logger.error(f"Failed to remove job {job_id}: {e}")
            return False
    
    def list_jobs(self) -> Dict[str, Dict[str, Any]]:
        return self.jobs.copy()


scheduler = SchedulerPlugin()
