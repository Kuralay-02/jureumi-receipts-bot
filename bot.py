import os
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))

# ---------- КНОПКА ----------
keyboard = ReplyKeyboardMarkup(
    [[KeyboardButton("📎 Отправить чек")]],
    resize_keyboard=True
)

# ---------- /start ----------
def start(update: Update, context: CallbackContext):
    text = (
        "Здравствуйте!\n\n"
        "Пожалуйста, отправляя чек, укажите:\n"
        "• за какую коробку произведена оплата\n"
        "• за какие позиции\n\n"
        "Если чек за несколько коробок — просто напишите об этом текстом.\n"
        "После этого нажмите кнопку ниже и прикрепите чек."
    )
    update.message.reply_text(text, reply_markup=keyboard)

# ---------- НАЖАТИЕ КНОПКИ ----------
def send_receipt_prompt(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Прикрепите чек (фото или файл).\n"
        "Если чек за несколько коробок — напишите это сообщением."
    )

# ---------- ПОЛУЧЕНИЕ ЧЕКА ----------
def handle_receipt(update: Update, context: CallbackContext):
    user = update.message.from_user

    username = f"@{user.username}" if user.username else "без username"
    name = user.full_name

    caption = (
        "🧾 НОВЫЙ ЧЕК\n\n"
        f"👤 {name}\n"
        f"🔗 {username}\n\n"
        "ℹ️ Проверь описание от клиента выше"
    )

    # Фото
    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        context.bot.send_photo(
            chat_id=ADMIN_CHAT_ID,
            photo=file_id,
            caption=caption
        )

    # Документ / PDF
    elif update.message.document:
        context.bot.send_document(
            chat_id=ADMIN_CHAT_ID,
            document=update.message.document.file_id,
            caption=caption
        )

    update.message.reply_text("Спасибо! Чек получен 🤍")

# ---------- MAIN ----------
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text("📎 Отправить чек"), send_receipt_prompt))
    dp.add_handler(MessageHandler(Filters.photo | Filters.document, handle_receipt))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
