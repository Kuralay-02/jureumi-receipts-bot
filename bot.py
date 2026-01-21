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
    "— за какую коробку\n"
    "— какие позиции\n"
    "— сумму\n\n"
    "Пример:\n"
    "@ваш_юз\n"
    "1 Корейская коробка\n"
    "#кор1 (название позиции)\n"
    "#кор2 (название позиции)\n"
    "Общая сумма к оплате\n\n"
    "Если вы оплатили за несколько коробок — укажите всё одним сообщением и "
    "отправьте одним чеком ❤️"
)

THANK_YOU_TEXT = (
    "✅ Чек принят!\n\n"
    "Я отправила его админу для проверки.\n\n"
    "Статус можно проверить в боте таблиц, попросив посчитать сумму доставки.\n"
    "Если чек принят — позиции к оплате исчезнут.\n\n"
    "⏳ Бот таблиц обновляется раз в три дня.\n\n"
    "Спасибо, что закупаетесь у нас ❤️"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(START_TEXT)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    caption_prefix = f"📩 ЧЕК ОТ @{user.username or user.id}\n\n"

    # если фото
    if update.message.photo:
        await context.bot.send_photo(
            chat_id=ADMIN_CHAT_ID,
            photo=update.message.photo[-1].file_id,
            caption=caption_prefix + (update.message.caption or "")
        )

    # если документ (pdf, скрин и т.п.)
    elif update.message.document:
        await context.bot.send_document(
            chat_id=ADMIN_CHAT_ID,
            document=update.message.document.file_id,
            caption=caption_prefix + (update.message.caption or "")
        )

    # если просто текст
    else:
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=caption_prefix + update.message.text
        )

    await update.message.reply_text(THANK_YOU_TEXT)


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_message))

    app.run_polling()


if __name__ == "__main__":
    main()
