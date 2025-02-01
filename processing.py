from telegram import Update
from telegram.ext import ContextTypes
import requests
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = '8132336276:AAG-fWxkD5RiRv3Z6aVPW_SOa--o0DgJUtc'

IMEI_CHECK_API_TOKEN = 'e4oEaZY1Kom5OXzybETkMlwjOCy3i8GSCGTHzWrhd4dc563b'

WHITELIST = {1799715497}

API_TOKEN = IMEI_CHECK_API_TOKEN


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Отправьте мне свой IMEI')

async def check_imei(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id

    if user_id not in WHITELIST:
        await update.message.reply_text('Доступ ограничен')
        return

    imei = update.message.text.strip()

    if not imei.isdigit() or len(imei) != 15:
        await update.message.reply_text('Некорректный IMEI. Убедитесь, что он состоит из 15 цифр.')
        return

    response = requests.post('https://imeicheck.net/api/check-imei', data={
        'imei': imei,
        'token': API_TOKEN
    })

    logger.info(f'Response from API: {response.status_code} - {response.text}')

    if response.status_code == 200:
        try:
            data = response.json()
            await update.message.reply_text(f'Информация о IMEI: {data}')
        except ValueError:
            await update.message.reply_text('Ошибка при обработке ответа от API. Не удалось распарсить JSON.')
    else:
        await update.message.reply_text('Ошибка при проверке IMEI. Попробуйте позже.')


