import unittest
from datetime import datetime
from src.engine.gold_monitor import GoldMonitor


class TestGoldMonitor(unittest.TestCase):
    def setUp(self):
        self.monitor = GoldMonitor()

    def test_is_within_buy_window(self):
        # Window is 20th - end of month
        self.assertTrue(
            self.monitor.is_within_buy_window(datetime(2026, 4, 20))
        )
        self.assertTrue(
            self.monitor.is_within_buy_window(datetime(2026, 4, 30))
        )
        self.assertFalse(
            self.monitor.is_within_buy_window(datetime(2026, 4, 19))
        )
        self.assertFalse(
            self.monitor.is_within_buy_window(datetime(2026, 4, 1))
        )

    def test_detect_dip_from_recent_history(self):
        # Current price is 1,220,000
        # History has prices 1,250,000, 1,245,000, 1,240,000
        history = [
            {"date": "2026-04-10", "price_idr": 1250000.0},
            {"date": "2026-04-11", "price_idr": 1245000.0},
            {"date": "2026-04-12", "price_idr": 1240000.0},
        ]
        current_price = 1220000.0

        # Penurunan > 1.5% dari harga kemarin (1,240,000 -> 1,220,000 is ~1.6%)
        is_dip, reason = self.monitor.analyze_price(current_price, history)
        self.assertTrue(is_dip)
        self.assertIn("koreksi", reason.lower())

    def test_detect_near_historical_low(self):
        # History has a low at 1,200,000
        history = [
            {"date": "2026-04-10", "price_idr": 1200000.0},
            {"date": "2026-04-11", "price_idr": 1210000.0},
            {"date": "2026-04-12", "price_idr": 1205000.0},
        ]
        current_price = 1202000.0  # Near low (within 1%)

        is_dip, reason = self.monitor.analyze_price(current_price, history)
        self.assertTrue(is_dip)
        self.assertIn("terendah", reason.lower())

    def test_no_dip_detected(self):
        history = [
            {"date": "2026-04-10", "price_idr": 1200000.0},
            {"date": "2026-04-11", "price_idr": 1190000.0},
        ]
        current_price = 1210000.0  # Price increasing

        is_dip, reason = self.monitor.analyze_price(current_price, history)
        self.assertFalse(is_dip)


if __name__ == "__main__":
    unittest.main()
