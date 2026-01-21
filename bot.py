from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
ADMIN_ID = int(os.environ["ADMIN_ID"])

START_TEXT = (
    "Здравствуйте!\n\n"
    "Чек оплаты за доставку коробок Джурыми до админа можете прислать сюда.\n\n"
    "Перед тем, как отправить чек, обязательно напишите:\n"
    "— за какую коробку\n"
    "— какие позиции\n"
    "— сумму\n\n"
    "Пример отправления чека:\n\n"
    "@ваш_юзернейм\n"
    "1 Корейская коробка (можете сокращать)\n"
    "#кор1 (название позиции)\n"
    "#кор2 (название позиции)\n"
    "Общая сумма к оплате\n\n"
    "Если вы оплатили за несколько коробок сразу, "
    "указывайте все одним текстом и отправьте одним чеком ❤️"
)

THANK_YOU_TEXT = (
    "Чек принят! ✅\n\n"
    "Присылаю админу для проверки.\n"
    "Статус можете проверить в боте таблицы, "
    "попросив посчитать сумму вашей доставки.\n\n"
    "Если чек принят, в боте таблицы ваши позиции к оплате исчезнут.\n"
    "❗ Бот таблицы обновляется раз в три дня!\n\n"
    "Спасибо, что закупаетесь у нас ❤️"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(START_TEXT)

async def forward_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # пересылаем сообщение админу как есть
    await update.message.forward(chat_id=ADMIN_ID)

    # благодарим пользователя
    await update.message.reply_text(THANK_YOU_TEXT)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, forward_check))

    app.run_polling()

if __name__ == "__main__":
    main()
