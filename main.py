import os
import logging
import asyncio
from datetime import datetime
from dotenv import load_dotenv

from src.engine.signal_filter import SignalScanner
from src.scheduler.service import MarketScheduler
from src.notifier.telegram import TelegramNotifier
from src.utils.stock_api import StockAPI
from src.utils.gold_api import GoldAPI
from src.utils.gold_storage import GoldStorage
from src.engine.gold_monitor import GoldMonitor
from src.utils.market_calendar import MarketCalendar

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


async def trigger_bsjp_scan(scanner, stock_api, notifier):
    """Execution logic for the 15:50 WIB BSJP scan."""
    if not MarketCalendar.is_market_open():
        logger.info("Market is closed (Holiday). Skipping BSJP scan.")
        return

    logger.info("Triggered BSJP Signal Scan...")

    # Fetch real-time data from Stockbit/IDX via Goapi
    data = stock_api.fetch_market_data()

    signals = scanner.filter_bsjp(data)

    if not signals:
        logger.info("Scan completed. No BSJP candidates found today.")
        return

    logger.info(f"Scan completed. Found {len(signals)} candidates.")
    for signal in signals:
        await notifier.send_bsjp_signal(signal)


async def trigger_market_update(stock_api, notifier, session_title):
    """Execution logic for scheduled market updates."""
    if not MarketCalendar.is_market_open():
        logger.info(
            f"Market is closed (Holiday). Skipping update: {session_title}"
        )
        return

    logger.info(f"Triggering Market Update: {session_title}")

    # Use real data to simulate market movers (Top 5)
    all_data = stock_api.fetch_market_data()
    sorted_data = sorted(
        all_data, key=lambda x: x["price_change_pct"], reverse=True
    )
    top_movers = sorted_data[:5]

    await notifier.send_market_update(session_title, top_movers)


async def trigger_gold_check(
    api, storage, monitor, notifier, current_date=None
):
    """Logic for daily gold price monitoring and dip alerts."""
    if not MarketCalendar.is_market_open():
        logger.info("Market is closed (Holiday). Skipping Gold check.")
        return

    if current_date is None:
        current_date = datetime.now()

    logger.info("Triggering Gold Price Check...")

    try:
        # 1. Fetch Price
        data = api.fetch_latest_price()
        current_price = data["price_idr_gram"]
        date_str = data["date"]

        # 2. Load History for Analysis
        history = storage.load_history()

        # 3. Analyze for Dips
        is_dip, reason = monitor.analyze_price(current_price, history)

        # 4. Save Today's Price
        storage.save_price(current_price, date_str)

        # 5. Determine Notification Type
        if monitor.is_within_buy_window(current_date) and is_dip:
            await notifier.send_gold_buy_alert(current_price, reason)
        else:
            # Calculate change for standard update
            change = 0
            if history:
                prev_price = history[-1].get("price_idr", 0)
                if prev_price > 0:
                    change = ((current_price - prev_price) / prev_price) * 100

            await notifier.send_gold_update(current_price, date_str, change)

    except Exception as e:
        logger.error(f"Gold Price Check failed: {e}")


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
    GOAPI_KEY = os.getenv("GOAPI_KEY")
    stock_api = StockAPI(api_key=GOAPI_KEY)

    scheduler.add_signal_job(
        trigger_bsjp_scan, args=(scanner, stock_api, notifier)
    )

    # 3. Add Market Status Jobs (Morning, Afternoon, Evening)
    scheduler.add_market_status_job(
        trigger_market_update,
        hour=9,
        minute=0,
        session_name="Morning",
        args=(stock_api, notifier, "Pagi"),
    )
    scheduler.add_market_status_job(
        trigger_market_update,
        hour=12,
        minute=0,
        session_name="Afternoon",
        args=(stock_api, notifier, "Siang"),
    )
    scheduler.add_market_status_job(
        trigger_market_update,
        hour=15,
        minute=50,
        session_name="Evening",
        args=(stock_api, notifier, "Sore"),
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

    # 6. Add Gold Monitoring Job (Daily 08:30 WIB)
    # Using environment variable for API Key
    gold_api = GoldAPI(api_key=GOAPI_KEY)
    gold_storage = GoldStorage()
    gold_monitor = GoldMonitor()

    scheduler.add_market_status_job(
        trigger_gold_check,
        hour=8,
        minute=30,
        session_name="GoldUpdate",
        args=(gold_api, gold_storage, gold_monitor, notifier),
    )

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
