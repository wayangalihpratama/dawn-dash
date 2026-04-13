import unittest
import os
import shutil
from src.utils.gold_storage import GoldStorage


class TestGoldStorage(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_data"
        self.test_file = os.path.join(self.test_dir, "gold_history.json")
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)
        self.storage = GoldStorage(storage_path=self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_save_price_creates_file(self):
        self.storage.save_price(1250000.0, "2026-04-13")
        self.assertTrue(os.path.exists(self.test_file))

    def test_save_and_retrieve_history(self):
        self.storage.save_price(1250000.0, "2026-04-12")
        self.storage.save_price(1235000.0, "2026-04-13")

        history = self.storage.load_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["price_idr"], 1250000.0)
        self.assertEqual(history[1]["date"], "2026-04-13")

    def test_prevent_duplicate_date(self):
        self.storage.save_price(1250000.0, "2026-04-13")
        self.storage.save_price(1260000.0, "2026-04-13")  # Same date

        history = self.storage.load_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["price_idr"], 1260000.0)  # Updated price

    def test_get_last_n_days(self):
        dates = ["2026-04-10", "2026-04-11", "2026-04-12", "2026-04-13"]
        for i, date in enumerate(dates):
            self.storage.save_price(1200000.0 + i, date)

        last_3 = self.storage.get_last_n_prices(3)
        self.assertEqual(len(last_3), 3)
        self.assertEqual(last_3[0]["date"], "2026-04-11")
        self.assertEqual(last_3[2]["date"], "2026-04-13")


if __name__ == "__main__":
    unittest.main()
