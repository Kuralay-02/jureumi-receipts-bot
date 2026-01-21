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
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))  # твой Telegram ID


START_TEXT = (
    "Здравствуйте!\n\n"
    "Чек оплаты за доставку коробок Джурыми до админа можете прислать сюда.\n\n"
    "Перед тем, как отправить чек, обязательно напишите:\n"
    "— за какую коробку\n"
    "— какие позиции\n"
    "— сумму\n\n"
    "📌 Пример отправления чека:\n"
    "@ваш_юз\n"
    "1 Корейская коробка\n"
    "#кор1 (название позиции)\n"
    "#кор2 (название позиции)\n"
    "Общая сумма к оплате\n\n"
    "Если вы оплатили за несколько коробок — указывайте всё одним текстом "
    "и отправляйте одним чеком ❤️"
)

THANKS_TEXT = (
    "✅ Чек принят!\n"
    "Присылаю админу для проверки.\n\n"
    "Статус можно проверить в боте таблиц, "
    "попросив посчитать сумму доставки.\n"
    "Если чек принят — позиции к оплате исчезнут.\n\n"
    "⏳ Бот таблиц обновляется раз в три дня.\n\n"
    "Спасибо, что закупаетесь у нас ❤️"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(START_TEXT)


async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # пересылаем админу ВСЁ сообщение как есть
    await context.bot.forward_message(
        chat_id=ADMIN_CHAT_ID,
        from_chat_id=update.message.chat_id,
        message_id=update.message.message_id,
    )

    await update.message.reply_text(THANKS_TEXT)


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(
            filters.TEXT | filters.PHOTO | filters.Document.ALL,
            forward_to_admin,
        )
    )

    app.run_polling()


if __name__ == "__main__":
    main()
