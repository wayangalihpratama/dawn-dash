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
                chat_id=self.chat_id,
                text=text,
                parse_mode=ParseMode.HTML,
            )
        except Exception as e:
            logger.error(f"Failed to send status report: {e}")

    async def send_market_update(self, session_title, stocks):
        """Sends a market overview with top gainers/losers."""
        message = f"<b>📊 Market Update: {session_title}</b>\n\n"

        for stock in stocks:
            symbol = stock.get("symbol")
            change = stock.get("price_change_pct")
            emoji = "🟢" if change >= 0 else "🔴"
            message += f"{emoji} <b>{symbol}</b>: {change:+.2f}%\n"

        message += "\n<i>Keep moving with Dawn Dash.</i>"

        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode=ParseMode.HTML,
            )
        except Exception as e:
            logger.error(f"Failed to send market update: {e}")

    async def send_gold_update(self, price, date, change):
        """Sends a standard daily gold price update."""
        status_emoji = "🟢" if change >= 0 else "🔴"
        change_text = f"{change:+.2f}%" if change != 0 else "Stagnan"

        message = (
            f"<b>🟡 Update Harga Emas</b>\n\n"
            f"💰 <b>Harga</b>: Rp {price:,.0f}/gram\n"
            f"📉 <b>Perubahan</b>: {status_emoji} {change_text}\n"
            f"📅 <b>Tanggal</b>: {date}\n\n"
            f"<i>Investasi rutin adalah kunci kekayaan jangka panjang.</i>"
        )

        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode=ParseMode.HTML,
            )
        except Exception as e:
            logger.error(f"Failed to send gold update: {e}")

    async def send_gold_buy_alert(self, price, reason):
        """Sends a priority buy alert when a gold dip is detected."""
        message = (
            f"<b>🚀 KESEMPATAN BELI EMAS!</b>\n\n"
            f"💰 <b>Harga Saat Ini</b>: Rp {price:,.0f}/gram\n"
            f"💡 <b>Analisis</b>: {reason}\n\n"
            f"Saran: Segera lakukan cicilan emas bulan ini sebelum harga memantul kembali."
        )

        keyboard = [
            [
                InlineKeyboardButton(
                    "🛒 Beli di Pegadaian",
                    url="https://www.pegadaian.co.id/produk/tabungan-emas",
                ),
                InlineKeyboardButton(
                    "🛒 Beli di Tokopedia",
                    url="https://www.tokopedia.com/emas/",
                ),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup,
            )
            logger.info("Gold buy alert sent to Telegram.")
        except Exception as e:
            logger.error(f"Failed to send gold buy alert: {e}")
