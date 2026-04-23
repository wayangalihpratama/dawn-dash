from datetime import datetime, date
import pytz


class MarketCalendar:
    """
    Utility to check if the IDX market is open.
    Covers weekends and 2026 public holidays for Indonesia Stock Exchange.
    """

    # IDX Holidays 2026 (Commonly known/estimated)
    # Note: These should be updated annually.
    IDX_HOLIDAYS_2026 = [
        date(2026, 1, 1),  # New Year
        date(2026, 1, 19),  # Isra Mi'raj
        date(2026, 2, 17),  # Chinese New Year
        date(2026, 3, 20),  # Nyepi
        date(2026, 3, 20),  # Eid al-Fitr (Estimated start)
        date(2026, 3, 21),  # Eid al-Fitr
        date(2026, 3, 22),  # Eid al-Fitr
        date(2026, 4, 3),  # Good Friday
        date(2026, 5, 1),  # Labor Day
        date(2026, 5, 14),  # Ascension of Christ
        date(2026, 5, 27),  # Vesak Day
        date(2026, 6, 1),  # Pancasila Day
        date(2026, 6, 15),  # Eid al-Adha
        date(2026, 7, 7),  # Islamic New Year
        date(2026, 8, 17),  # Independence Day
        date(2026, 9, 14),  # Prophet Muhammad's Birthday
        date(2026, 12, 25),  # Christmas
    ]

    @staticmethod
    def is_market_open(dt=None):
        """
        Checks if the market is open on a given datetime.
        Defaults to current Jakarta time.
        """
        if dt is None:
            jakarta_tz = pytz.timezone("Asia/Jakarta")
            dt = datetime.now(jakarta_tz)

        # 1. Check Weekend (Saturday=5, Sunday=6)
        if dt.weekday() >= 5:
            return False

        # 2. Check Public Holiday
        if dt.date() in MarketCalendar.IDX_HOLIDAYS_2026:
            return False

        return True

    @staticmethod
    def get_market_status_msg():
        """Returns a string describing why the market is closed or 'Open'."""
        jakarta_tz = pytz.timezone("Asia/Jakarta")
        dt = datetime.now(jakarta_tz)

        if dt.weekday() == 5:
            return "Closed (Saturday)"
        if dt.weekday() == 6:
            return "Closed (Sunday)"
        if dt.date() in MarketCalendar.IDX_HOLIDAYS_2026:
            return "Closed (IDX Holiday)"

        return "Open"
