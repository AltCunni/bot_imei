import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from processing import start, check_imei
from config import TELEGRAM_TOKEN


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_imei))

    app.run_polling()


if __name__ == '__main__':
    main()
