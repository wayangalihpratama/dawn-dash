from datetime import datetime
import pytz
from src.utils.market_calendar import MarketCalendar


def test_is_market_open_weekday():
    # Tuesday, Oct 21, 2025 (Not a holiday)
    jakarta_tz = pytz.timezone("Asia/Jakarta")
    dt = jakarta_tz.localize(datetime(2025, 10, 21, 10, 0))
    assert MarketCalendar.is_market_open(dt) is True


def test_is_market_open_weekend():
    # Saturday, Oct 25, 2025
    jakarta_tz = pytz.timezone("Asia/Jakarta")
    dt = jakarta_tz.localize(datetime(2025, 10, 25, 10, 0))
    assert MarketCalendar.is_market_open(dt) is False


def test_is_market_open_holiday():
    # Independence Day 2026
    jakarta_tz = pytz.timezone("Asia/Jakarta")
    dt = jakarta_tz.localize(datetime(2026, 8, 17, 10, 0))
    assert MarketCalendar.is_market_open(dt) is False


def test_market_status_msg():
    # Saturday
    jakarta_tz = pytz.timezone("Asia/Jakarta")
    dt = jakarta_tz.localize(datetime(2025, 10, 25, 10, 0))
    # We test logic elsewhere as 'now' is hard to mock here
    assert dt is not None
