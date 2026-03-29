import logging
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

logger = logging.getLogger(__name__)


class MarketScheduler:
    def __init__(self, timezone="Asia/Jakarta"):
        self.tz = pytz.timezone(timezone)
        self.scheduler = AsyncIOScheduler(timezone=self.tz)

    def add_signal_job(self, func, args=None, hour=15, minute=50):
        """Adds a job to scan for BSJP signals."""
        trigger = CronTrigger(hour=hour, minute=minute, timezone=self.tz)
        self.scheduler.add_job(
            func, trigger, args=args, name="BSJP_Signal_Scan"
        )
        logger.info(
            f"Scheduled 'BSJP Signal Scan' at {hour:02d}:{minute:02d} "
            f"timezone: {self.tz}"
        )

    def add_journal_job(self, func, args=None, hour=17, minute=00):
        """Adds a job to generate the daily learning journal."""
        trigger = CronTrigger(hour=hour, minute=minute, timezone=self.tz)
        self.scheduler.add_job(func, trigger, args=args, name="Daily_Journal")
        logger.info(
            f"Scheduled 'Daily Journal' at {hour:02d}:{minute:02d} {self.tz}"
        )

    def add_exit_job(self, func, args=None, hour=9, minute=00):
        """Adds a job to notify about automated exits at market open."""
        trigger = CronTrigger(hour=hour, minute=minute, timezone=self.tz)
        self.scheduler.add_job(func, trigger, args=args, name="Automated_Exit")
        logger.info(
            f"Scheduled 'Automated Exit' at {hour:02d}:{minute:02d} {self.tz}"
        )

    def add_market_status_job(self, func, hour, minute, session_name, args=None):
        """Adds a generic market status/price check job."""
        trigger = CronTrigger(hour=hour, minute=minute, timezone=self.tz)
        job_name = f"PriceCheck_{session_name}"
        self.scheduler.add_job(func, trigger, args=args, name=job_name)
        logger.info(
            f"Scheduled 'Price Check: {session_name}' at "
            f"{hour:02d}:{minute:02d} {self.tz}"
        )

    def start(self):
        """Starts the background scheduler."""
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("Market Scheduler (AsyncIO) Started.")

    def shutdown(self):
        """Shuts down the scheduler."""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Market Scheduler Shutdown.")
