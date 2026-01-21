import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))

# ---------- ТЕКСТ И КНОПКА ----------
START_TEXT = (
    "Здравствуйте!\n\n"
    "Чек оплаты за доставку коробок Джурыми до админа можете прислать сюда.\n\n"
    "Перед тем, как отправить чек, обязательно напишите:\n"
    "• оплата за какую коробку\n"
    "• какие позиции\n"
    "• сумму\n\n"
    "Если вы оплатили за несколько коробок — указывайте всё одним текстом "
    "и отправьте одним чеком ❤️"
)

keyboard = ReplyKeyboardMarkup(
    [["Отправить чек"]],
    resize_keyboard=True
)

# ---------- /start И КНОПКА ----------
def start(update: Update, context: CallbackContext):
    update.message.reply_text(START_TEXT, reply_markup=keyboard)

def show_instruction(update: Update, context: CallbackContext):
    start(update, context)

# ---------- ПРИЁМ ЧЕКА ----------
def handle_receipt(update: Update, context: CallbackContext):
    user = update.message.from_user
    username = f"@{user.username}" if user.username else "без username"
    name = user.full_name

    caption = (
        "🧾 НОВЫЙ ЧЕК\n\n"
        f"👤 {name}\n"
        f"🔗 {username}\n\n"
        "ℹ️ Описание от клиента смотрите выше"
    )

    if update.message.photo:
        context.bot.send_photo(
            chat_id=ADMIN_CHAT_ID,
            photo=update.message.photo[-1].file_id,
            caption=caption
        )

    elif update.message.document:
        context.bot.send_document(
            chat_id=ADMIN_CHAT_ID,
            document=update.message.document.file_id,
            caption=caption
        )

    update.message.reply_text(
        "Чек принят! Присылаю админу для проверки.\n\n"
        "Статус можно проверить в боте таблиц.\n"
        "Спасибо, что закупаетесь у нас ❤️"
    )

# ---------- MAIN ----------
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & Filters.regex("^Отправить чек$"), show_instruction))
    dp.add_handler(MessageHandler(Filters.photo | Filters.document, handle_receipt))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
