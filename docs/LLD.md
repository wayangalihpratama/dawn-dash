# Dawn Dash: Low-Level Design (LLD) [#1]

## 1. System Overview
Dawn Dash is a Python-based utility container designed to bridge Stockbit screener results with a Telegram bot interface. It uses a scheduled execution model (cron or Python `apscheduler`) to process data and notify the user at specific Indonesian Market (BEI) times.

## 2. Technical Stack
- **Language**: Python 3.11+
- **Containerization**: Docker + Docker Compose
- **Platform**: Telegram (API via `python-telegram-bot`)
- **Execution Architecture**: Singleton worker service.

## 3. Module Decomposition

### 3.1. Scheduler Module
- Responsible for triggering signal checks based on BEI Market Hours:
    - 15:50 WIB: BSJP Screening (Buy)
    - 17:00 WIB: Daily Journal Generation
    - 09:00 WIB: Profit/Loss Notification

### 3.2. Signal Engine
- Filters stock data (simulated/manual/API).
- Criteria: `Volume > 1.5x Avg`, `Price > +2%`, `Index in KOMPAS100`.

### 3.3. Notification Module (Telegram)
- Formats and sends messages with inline action buttons.
- **Deep-Link Strategy**: Uses Universal Links (`https://stockbit.com/symbol/[TICKER]`) to ensure the mobile app opens directly via OS-level redirection.
- Handles incoming commands: `/start`, `/ping`, `/status`.

---

## 4. Environment & Security
- **Config**: `.env` file (never committed).
- **Secrets**: `TELEGRAM_BOT_TOKEN`, `CHAT_ID`.
- **Docker Strategy**: 
    - Multi-stage build for a slim production image.
    - Volume mount for local development.

---

## 5. Integration: Stockbit Deep-Linking
- **Format**: `https://stockbit.com/symbol/[TICKER]`
- **Behavior**: On mobile devices with Stockbit installed, this URL triggers a Universal/App Link redirect to the in-app ticker page. On desktop, it opens the web interface.
- **Bibit Integration**: Similar URL patterns for mutual funds or direct portfolio views where available.

---

## 6. Development Workflow
- **Linting**: Black/Flake8. 
- **Testing**: Pytest for signal logic.
- **Commands**:
    - **Startup**: `./dc.sh up -d` (Runs in background)
    - **Rebuild**: `./dc.sh up -d --build`
    - **Logs**: `./dc.sh logs -f`
    - **Shutdown**: `./dc.sh down`
    - **Run Tests**: `./dc.sh run --rm bot python -m pytest tests/`
