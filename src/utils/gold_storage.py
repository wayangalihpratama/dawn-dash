import json
import os
import logging

logger = logging.getLogger(__name__)


class GoldStorage:
    def __init__(self, storage_path="data/gold_history.json"):
        self.storage_path = storage_path
        self._ensure_dir()

    def _ensure_dir(self):
        """Ensures the directory for the storage file exists."""
        directory = os.path.dirname(self.storage_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

    def load_history(self):
        """Loads price history from the JSON file."""
        if not os.path.exists(self.storage_path):
            return []

        try:
            with open(self.storage_path, "r") as f:
                data = json.load(f)
                return data.get("history", [])
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Failed to load gold history: {e}")
            return []

    def save_price(self, price_idr, date_str):
        """
        Saves a daily price to the history.
        Updates if the date already exists.
        """
        history = self.load_history()

        # Check if date already exists
        updated = False
        for entry in history:
            if entry.get("date") == date_str:
                entry["price_idr"] = price_idr
                updated = True
                break

        if not updated:
            history.append({"date": date_str, "price_idr": price_idr})

        # Sort by date to maintain chronological order
        history.sort(key=lambda x: x["date"])

        try:
            with open(self.storage_path, "w") as f:
                json.dump(
                    {"last_updated": date_str, "history": history}, f, indent=2
                )
        except IOError as e:
            logger.error(f"Failed to save gold price: {e}")
            raise

    def get_last_n_prices(self, n):
        """Returns the last N historical price entries."""
        history = self.load_history()
        return history[-n:] if history else []
