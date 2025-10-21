from telegram.ext import Application
from interfaces.telegram_bot import start, handle_voice
from config import BOT_TOKEN
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from interfaces.telegram_bot import start, handle_voice

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    print("Бот запущен.")
    app.run_polling()

if __name__ == "__main__":
    main()