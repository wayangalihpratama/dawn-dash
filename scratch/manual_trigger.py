import os
import asyncio
import logging
import json
from datetime import datetime
from dotenv import load_dotenv

from src.engine.signal_filter import SignalScanner
from src.notifier.telegram import TelegramNotifier
from src.utils.stock_api import StockAPI
from src.utils.pegadaian_api import PegadaianAPI
from src.utils.gold_storage import GoldStorage
from src.engine.gold_monitor import GoldMonitor

# Setup Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def run_manual_trigger():
    """
    Manually triggers both Stock (BSJP) and Gold analysis,
    bypassing the MarketCalendar holiday checks.
    """
    load_dotenv()
    GOAPI_KEY = os.getenv("GOAPI_KEY")
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")

    if not BOT_TOKEN or not CHAT_ID:
        logger.error("TELEGRAM_BOT_TOKEN or CHAT_ID not set in .env")
        return

    notifier = TelegramNotifier(BOT_TOKEN, CHAT_ID)
    print("\n" + "=" * 40)
    print("🚀 DAWN DASH MANUAL TRIGGER")
    print("=" * 40)

    # --- 1. Gold Analysis ---
    print("\n[1/2] 🌕 RUNNING GOLD ANALYSIS...")
    try:
        api = PegadaianAPI()
        storage = GoldStorage()
        monitor = GoldMonitor()

        # Fetch
        data = api.fetch_latest_price()
        current_price = data["price_idr_gram"]
        date_str = data["date"]
        print(f"Current Gold Price: Rp {current_price:,.0f} ({date_str})")

        # Analyze
        history = storage.load_history()
        is_dip, reason = monitor.analyze_price(current_price, history)

        # Save
        storage.save_price(current_price, date_str)

        # Notify
        if is_dip:
            print(f"⚠️ DIP DETECTED: {reason}")
            await notifier.send_gold_buy_alert(current_price, reason)
        else:
            print("✅ Price is stable.")
            # Calculate change for update
            change = 0
            if history:
                prev = history[-1].get("price_idr", 0)
                if prev > 0:
                    change = ((current_price - prev) / prev) * 100
            await notifier.send_gold_update(current_price, date_str, change)
        print("✅ Gold check complete.")
    except Exception as e:
        logger.error(f"Gold check failed: {e}", exc_info=True)

    # --- 2. Stock Analysis ---
    print("\n[2/2] 📈 RUNNING STOCK BSJP ANALYSIS...")
    try:
        stock_api = StockAPI(api_key=GOAPI_KEY)
        scanner = SignalScanner()

        # Fetch
        print("Fetching market data...")
        all_data = stock_api.fetch_market_data()
        print(f"Fetched {len(all_data)} stocks.")

        # Filter
        signals = scanner.filter_bsjp(all_data)

        # Notify
        if not signals:
            print("❌ No BSJP signals found today.")
            # Still send a small status update if requested, but usually skip
        else:
            print(f"✅ Found {len(signals)} signals!")
            for signal in signals:
                print(f" - {signal['symbol']}: {signal['price_change_pct']}%")
                await notifier.send_bsjp_signal(signal)

        # Debug: Show Top Movers anyway
        sorted_movers = sorted(
            all_data, key=lambda x: x.get("price_change_pct", 0), reverse=True
        )
        print("\n--- Top 5 Market Movers (Debug) ---")
        for stock in sorted_movers[:5]:
            print(f"{stock['symbol']}: {stock['price_change_pct']}%")

        print("✅ Stock check complete.")
    except Exception as e:
        logger.error(f"Stock check failed: {e}", exc_info=True)

    print("\n" + "=" * 40)
    print("✨ ALL MANUAL TASKS COMPLETE")
    print("=" * 40 + "\n")


if __name__ == "__main__":
    asyncio.run(run_manual_trigger())
