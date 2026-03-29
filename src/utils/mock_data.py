import random


def get_mock_stock_data():
    """
    Simulates a list of KOMPAS100 stocks with random price and volume data.
    Ensures at least one stock (typically BBCA or BREN)
    triggers the BSJP criteria.
    """
    tickers = [
        "ARCI",
        "BKSL",
        "BREN",
        "BULL",
        "BUVA",
        "CBDK",
        "CUAN",
        "HRTA",
        "IMPC",
        "INET",
        "PSAB",
        "RATU",
        "SGER",
        "SMIL",
        "TOBA",
        "WIFI",
        "WIRG",
        "BBCA",
        "BBRI",
        "BMRI",
        "BBNI",
        "ASII",
        "TLKM",
        "UNTR",
        "BRMS",
        "ADRO",
        "ITMG",
        "PTBA",
        "INCO",
        "ANTM",
    ]

    data = []
    for ticker in tickers:
        # Most stocks are quiet
        price_change = round(random.uniform(-1, 1.5), 2)
        vol_ratio = round(random.uniform(0.5, 1.2), 2)

        # Inject a winner (e.g., BBCA or BREN)
        if ticker in ["BBCA", "BREN"] and random.choice([True, False]):
            price_change = round(random.uniform(2.1, 4.5), 2)
            vol_ratio = round(random.uniform(1.6, 3.0), 2)

        avg_vol = 1000000
        data.append(
            {
                "symbol": ticker,
                "price_change_pct": price_change,
                "volume": int(avg_vol * vol_ratio),
                "avg_volume_20": avg_vol,
            }
        )

    return data
