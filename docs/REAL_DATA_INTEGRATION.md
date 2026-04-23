# Feature: Real-Time Market Data Integration [#2]

## 1. Overview
Transition the Dawn Dash bot from mock/static data to live market data using Goapi.io. This includes both Stock (IDX) and Gold (Pegadaian) data streams.

## 2. Implementation Details

### 2.1. Stock API Integration
- **Provider**: Goapi.io
- **Endpoint**: `/stock/idx/trending`
- **Authentication**: `X-API-KEY` header.
- **Mapping**: Data is mapped to `symbol`, `price_change_pct`, and `volume`.
- **Fallbacks**: If a stock is missing 20-day average volume from the API, it defaults to a baseline (1,000,000) to ensure the scanner logic still functions.

### 2.2. Gold Price Integration (Pegadaian)
- **Provider**: Pegadaian (Official Internal API)
- **Endpoint**: `https://sahabat.pegadaian.co.id/gold/prices/savings`
- **Logic**: Fetches the "Tabungan Emas" daily rate. We prioritize the `buy` price for signal generation.
- **Fallbacks**: Uses the last cached successful price if the API fails.

### 2.3. Market Holiday Logic
- **Module**: `MarketCalendar`
- **Behavior**: Proactively detects weekends and 2026 IDX holidays.
- **Impact**: All scheduled scans and updates are skipped when the market is closed, reducing API consumption and avoiding flat signals.

## 3. Testing Status
- **Unit Tests**: `tests/test_stock_api.py`, `tests/test_market_calendar.py`, and `tests/test_pegadaian_api.py`.
- **Manual Verification**: Verified via `scratch/run_analysis.py` and `scratch/test_gold.py`.

## 4. Known Limitations
- **API Availability**: Internal APIs may lack formal SLA; implementation includes robust error handling and user-agent spoofing to maintain connectivity.

