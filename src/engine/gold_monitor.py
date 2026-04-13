import logging

logger = logging.getLogger(__name__)


class GoldMonitor:
    def __init__(self, dip_threshold=0.015, near_low_threshold=0.01):
        """
        :param dip_threshold: Percentage drop from yesterday to trigger
            an alert (default 1.5%)
        :param near_low_threshold: Percentage within historical low
            to trigger an alert (default 1%)
        """
        self.dip_threshold = dip_threshold
        self.near_low_threshold = near_low_threshold

    def is_within_buy_window(self, current_date):
        """Checks if the current date is within the 20th - end of month window."""
        return current_date.day >= 20

    def analyze_price(self, current_price, history):
        """
        Analyzes the current price against history to detect dips.
        Returns (is_dip, reason).
        """
        if not history:
            return False, "Insufficient history"

        # 1. Check for Drop from Yesterday
        yesterday_price = history[-1].get("price_idr", 0)
        if yesterday_price > 0:
            change = (current_price - yesterday_price) / yesterday_price
            if change <= -self.dip_threshold:
                return (
                    True,
                    f"Koreksi harga tajam ({round(change*100, 2)}%) dibanding kemarin.",
                )

        # 2. Check for Near Historical Low (last 30 entries)
        prices_only = [
            h.get("price_idr", 0) for h in history if h.get("price_idr", 0) > 0
        ]
        if prices_only:
            historic_low = min(prices_only)
            # If current price is within X% of the historic low
            if current_price <= historic_low * (1 + self.near_low_threshold):
                if current_price < historic_low:
                    return (
                        True,
                        "Harga mencapai titik terendah baru tahun ini!",
                    )
                return (
                    True,
                    "Harga mendekati titik terendah dalam periode terakhir.",
                )

        return False, "Stable"
