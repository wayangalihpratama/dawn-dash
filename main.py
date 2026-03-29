import os
import logging
import asyncio
from dotenv import load_dotenv

from src.engine.signal_filter import SignalScanner
from src.scheduler.service import MarketScheduler
from src.notifier.telegram import TelegramNotifier
from src.utils.mock_data import get_mock_stock_data

# --- Configuration ---
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


# --- Logging ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def trigger_bsjp_scan(scanner, notifier):
    """Execution logic for the 15:50 WIB BSJP scan."""
    logger.info("Triggered BSJP Signal Scan...")

    # In a real scenario, this would fetch from an API.
    # For MVP, we use mock data.
    data = get_mock_stock_data()

    signals = scanner.filter_bsjp(data)

    if not signals:
        logger.info("Scan completed. No BSJP candidates found today.")
        return

    logger.info(f"Scan completed. Found {len(signals)} candidates.")
    for signal in signals:
        await notifier.send_bsjp_signal(signal)


async def trigger_market_update(notifier, session_title):
    """Execution logic for scheduled market updates."""
    logger.info(f"Triggering Market Update: {session_title}")

    # Use mock data to simulate market movers (Top 5)
    all_data = get_mock_stock_data()
    sorted_data = sorted(
        all_data, key=lambda x: x["price_change_pct"], reverse=True
    )
    top_movers = sorted_data[:5]

    await notifier.send_market_update(session_title, top_movers)


async def main():
    logger.info("Dawn Dash Bot Starting (Integrated)...")

    if not TELEGRAM_BOT_TOKEN or not CHAT_ID:
        logger.error(
            "TELEGRAM_BOT_TOKEN or CHAT_ID not set. Please check .env."
        )
        return

    # 1. Initialize Components
    scanner = SignalScanner()
    notifier = TelegramNotifier(TELEGRAM_BOT_TOKEN, CHAT_ID)
    scheduler = MarketScheduler()

    # 2. Add Market Jobs (Passing Functions Directly - No Lambdas)
    scheduler.add_signal_job(trigger_bsjp_scan, args=(scanner, notifier))

    # 3. Add Market Status Jobs (Morning, Afternoon, Evening)
    scheduler.add_market_status_job(
        trigger_market_update,
        hour=9,
        minute=0,
        session_name="Morning",
        args=(notifier, "Pagi"),
    )
    scheduler.add_market_status_job(
        trigger_market_update,
        hour=12,
        minute=0,
        session_name="Afternoon",
        args=(notifier, "Siang"),
    )
    scheduler.add_market_status_job(
        trigger_market_update,
        hour=15,
        minute=50,
        session_name="Evening",
        args=(notifier, "Sore"),
    )

    # 4. Start Scheduler
    scheduler.start()

    # 5. Final Notification
    logger.info(
        "Bot is active and listening for market events. Press Ctrl+C to stop."
    )
    await notifier.send_status_report(
        "🚀 <b>Dawn Dash Bot Started!</b>\n"
        "Market Scheduler is active for WIB hours."
    )

    # 6. Manual Smoke Test (Full Session Verification)
    logger.info("Running manual smoke tests for all sessions...")
    await trigger_market_update(notifier, "Pagi (Smoke Test)")
    await trigger_market_update(notifier, "Siang (Smoke Test)")
    await trigger_market_update(notifier, "Sore (Smoke Test)")

    # 7. Continuous Execution Loop
    try:
        while True:
            await asyncio.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot shutting down...")
        scheduler.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")
