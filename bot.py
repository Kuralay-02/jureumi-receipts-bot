import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))

START_TEXT = (
    "Здравствуйте!\n\n"
    "Чек оплаты за доставку коробок Джурыми до админа можете прислать сюда.\n\n"
    "Перед тем, как отправить чек, обязательно напишите:\n"
    "• за какую коробку\n"
    "• какие позиции\n"
    "• сумму\n\n"
    "Пример:\n"
    "@вашюзер\n"
    "1 Корейская коробка\n"
    "#кор1 (название позиции)\n"
    "#кор2 (название позиции)\n"
    "Общая сумма\n\n"
    "Если оплатили несколько коробок — укажите всё одним сообщением ❤️"
)

THANK_YOU_TEXT = (
    "Чек принят! ✅\n\n"
    "Я переслала его админу для проверки.\n"
    "Статус можно проверить в боте таблиц.\n\n"
    "Спасибо, что закупаетесь у нас ❤️"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(START_TEXT)


async def handle_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    # Пересылаем админу ВСЁ как есть
    await message.forward(chat_id=ADMIN_CHAT_ID)

    # Благодарим пользователя
    await message.reply_text(THANK_YOU_TEXT)


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_receipt))

    app.run_polling()


if __name__ == "__main__":
    main()
