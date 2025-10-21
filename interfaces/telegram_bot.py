import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from core.lecture_pipeline import run_lecture_pipeline
from utils.file_manager import create_temp_file

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎓 Отправьте голосовое сообщение — я сделаю конспект лекции!"
    )

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    await context.bot.send_chat_action(chat_id=message.chat_id, action="typing")

    temp_path = create_temp_file()
    try:
        # Скачивание
        voice_file = await message.voice.get_file()
        await voice_file.download_to_drive(temp_path)

        # Запуск пайплайна в фоне (не блокируем event loop)
        loop = asyncio.get_event_loop()
        summary = await loop.run_in_executor(None, run_lecture_pipeline, str(message.from_user.id), temp_path)

        await message.reply_text(f"**Конспект лекции:**\n\n{summary}", parse_mode="Markdown")

    except Exception as e:
        error_msg = f"Ошибка: {str(e)}"
        print(error_msg)
        await message.reply_text(error_msg)