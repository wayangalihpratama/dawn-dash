import unittest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
from datetime import datetime
from src.utils.gold_api import GoldAPI
from src.utils.gold_storage import GoldStorage
from src.engine.gold_monitor import GoldMonitor
from src.notifier.telegram import TelegramNotifier


class TestIntegrationGold(unittest.TestCase):
    def setUp(self):
        # We need to use AsyncMock for TelegramNotifier as its methods are async
        self.notifier = MagicMock(spec=TelegramNotifier)
        self.notifier.send_gold_update = AsyncMock()
        self.notifier.send_gold_buy_alert = AsyncMock()

        self.api = MagicMock(spec=GoldAPI)
        self.storage = MagicMock(spec=GoldStorage)
        self.monitor = GoldMonitor()

    def test_trigger_gold_check_normal_day(self):
        # Setup: It's the 10th (outside window), price is stable
        current_date = datetime(2026, 4, 10)
        price_data = {"price_idr_gram": 1250000.0, "date": "2026-04-10"}
        self.api.fetch_latest_price.return_value = price_data
        self.storage.load_history.return_value = [
            {"date": "2026-04-09", "price_idr": 1250000.0}
        ]

        # Action: We'll call the trigger function (to be implemented in main.py)
        # For now, let's simulate the logic that will be in main.py
        from main import trigger_gold_check

        asyncio.run(
            trigger_gold_check(
                self.api,
                self.storage,
                self.monitor,
                self.notifier,
                current_date,
            )
        )

        # Verify: send_gold_update called, but NOT send_gold_buy_alert
        self.notifier.send_gold_update.assert_called_once()
        self.notifier.send_gold_buy_alert.assert_not_called()
        self.storage.save_price.assert_called_once_with(
            1250000.0, "2026-04-10"
        )

    def test_trigger_gold_check_buy_alert(self):
        # Setup: It's the 25th (inside window), price dropped 2%
        current_date = datetime(2026, 4, 25)
        price_data = {"price_idr_gram": 1200000.0, "date": "2026-04-25"}
        self.api.fetch_latest_price.return_value = price_data
        self.storage.load_history.return_value = [
            {"date": "2026-04-24", "price_idr": 1230000.0}
        ]

        from main import trigger_gold_check

        asyncio.run(
            trigger_gold_check(
                self.api,
                self.storage,
                self.monitor,
                self.notifier,
                current_date,
            )
        )

        # Verify: send_gold_buy_alert is called due to > 1.5% drop in window
        self.notifier.send_gold_buy_alert.assert_called_once()
        self.storage.save_price.assert_called_once()


if __name__ == "__main__":
    unittest.main()
