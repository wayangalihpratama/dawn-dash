import logging
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode

logger = logging.getLogger(__name__)


class TelegramNotifier:
    def __init__(self, token, chat_id):
        self.bot = Bot(token=token)
        self.chat_id = chat_id

    async def send_bsjp_signal(self, signal):
        """
        Sends a BSJP buy signal to Telegram.
        :param signal: Dict with 'symbol', 'price_change_pct', 'volume_ratio'
        """
        ticker = signal.get("symbol")
        change = signal.get("price_change_pct")
        ratio = signal.get("volume_ratio")

        # 1. Format Message (HTML)
        message = (
            f"<b>🚩 Target BSJP Ditemukan: {ticker}</b>\n\n"
            f"📈 <b>Price Change</b>: +{change}%\n"
            f"📊 <b>Volume Ratio</b>: {ratio}x Avg\n"
            f"🔍 <b>Logic</b>: High Momentum (BSJP Signal)\n\n"
            f"<i>Klik tombol di bawah untuk beli langsung di Stockbit.</i>"
        )

        # 2. Universal Link Inline Button
        # Format: https://stockbit.com/symbol/[TICKER]
        stockbit_url = f"https://stockbit.com/symbol/{ticker}"
        keyboard = [
            [InlineKeyboardButton("🛒 Beli di Stockbit", url=stockbit_url)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # 3. Handle Notification
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup,
            )
            logger.info(f"Signal sent to Telegram for {ticker}.")
        except Exception as e:
            logger.error(f"Failed to send Telegram signal: {e}")

    async def send_status_report(self, text):
        """Sends a generic status report or journal to Telegram."""
        try:
            await self.bot.send_message(
                chat_id=self.chat_id, text=text, parse_mode=ParseMode.HTML
            )
        except Exception as e:
            logger.error(f"Failed to send status report: {e}")
