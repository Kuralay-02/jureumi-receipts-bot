import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))

START_TEXT = (
    "Здравствуйте! Чек оплаты за доставку коробок Джурыми до админа можете прислать сюда.\n\n"
    "Перед тем, как отправить чек, обязательно напишите:\n"
    "— оплата за какую коробку\n"
    "— какие позиции\n"
    "— сумму\n\n"
    "Пример:\n"
    "@ваш_юзернейм\n"
    "1 Корейская коробка\n"
    "#кор1 (название позиции)\n"
    "#кор2 (название позиции)\n"
    "Общая сумма\n\n"
    "Если оплатили за несколько коробок — указывайте всё одним сообщением ❤️"
)

CONFIRM_TEXT = (
    "Чек принят! Присылаю админу для проверки.\n\n"
    "Статус можно проверить в боте таблиц — "
    "если чек принят, позиции исчезнут.\n\n"
    "Бот обновляется раз в три дня.\n\n"
    "Спасибо, что закупаетесь у нас ❤️"
)

def start(update: Update, context: CallbackContext):
    update.message.reply_text(START_TEXT)

def handle_receipt(update: Update, context: CallbackContext):
    # пересылаем админу сообщение + файл
    context.bot.forward_message(
        chat_id=ADMIN_CHAT_ID,
        from_chat_id=update.message.chat_id,
        message_id=update.message.message_id
    )

    update.message.reply_text(CONFIRM_TEXT)

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.all & ~Filters.command, handle_receipt))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
