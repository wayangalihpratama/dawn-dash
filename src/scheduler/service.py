import logging
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

logger = logging.getLogger(__name__)


class MarketScheduler:
    def __init__(self, timezone="Asia/Jakarta"):
        self.tz = pytz.timezone(timezone)
        self.scheduler = BackgroundScheduler(timezone=self.tz)

    def add_signal_job(self, func, hour=15, minute=50):
        """Adds a job to scan for BSJP signals."""
        trigger = CronTrigger(hour=hour, minute=minute, timezone=self.tz)
        self.scheduler.add_job(func, trigger, name="BSJP_Signal_Scan")
        logger.info(
            f"Scheduled 'BSJP Signal Scan' at {hour:02d}:{minute:02d} {self.tz}"
        )

    def add_journal_job(self, func, hour=17, minute=00):
        """Adds a job to generate the daily learning journal."""
        trigger = CronTrigger(hour=hour, minute=minute, timezone=self.tz)
        self.scheduler.add_job(func, trigger, name="Daily_Journal")
        logger.info(
            f"Scheduled 'Daily Journal' at {hour:02d}:{minute:02d} {self.tz}"
        )

    def add_exit_job(self, func, hour=9, minute=00):
        """Adds a job to notify about automated exits at market open."""
        trigger = CronTrigger(hour=hour, minute=minute, timezone=self.tz)
        self.scheduler.add_job(func, trigger, name="Automated_Exit")
        logger.info(
            f"Scheduled 'Automated Exit' at {hour:02d}:{minute:02d} {self.tz}"
        )

    def start(self):
        """Starts the background scheduler."""
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("Market Scheduler Started.")

    def shutdown(self):
        """Shuts down the scheduler."""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Market Scheduler Shutdown.")
