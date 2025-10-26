import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from core.lecture_pipeline import run_lecture_pipeline
from utils.file_manager import create_temp_file_with_suffix

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Отправьте голосовое, аудио или видео (MP4) — я сделаю конспект лекции!"
    )

async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    await context.bot.send_chat_action(chat_id=message.chat_id, action="typing")

    # Определяем тип медиа и получаем файл + расширение
    file = None
    file_ext = ".ogg"  # по умолчанию для голосовых

    if message.voice:
        file = await message.voice.get_file()
        file_ext = ".ogg"
    elif message.video:
        file = await message.video.get_file()
        file_ext = ".mp4"
    elif message.audio:
        file = await message.audio.get_file()
        # Пытаемся угадать расширение по MIME или имени
        mime_type = getattr(message.audio, "mime_type", "") or ""
        if "mp4" in mime_type or "m4a" in mime_type:
            file_ext = ".m4a"
        elif "mp3" in mime_type:
            file_ext = ".mp3"
        else:
            file_ext = ".ogg"
    else:
        await message.reply_text("Пожалуйста, отправьте голосовое, аудио или видео.")
        return

    # Создаём временный файл с правильным расширением
    temp_path = create_temp_file_with_suffix(file_ext)

    try:
        # Скачиваем
        await file.download_to_drive(temp_path)

        # Запускаем пайплайн
        loop = asyncio.get_event_loop()
        summary_chunks = await loop.run_in_executor(None, run_lecture_pipeline, str(message.from_user.id), temp_path)

        # Формируем ответ
        if isinstance(summary_chunks, list):
            full_text = "\n\n".join(
                f"**Часть {i+1}:**\n{chunk['summary']}"
                for i, chunk in enumerate(summary_chunks)
            )
        else:
            full_text = summary_chunks  # на случай старой версии

        await message.reply_text(f"**Конспект лекции:**\n\n{full_text}", parse_mode="Markdown")

    except Exception as e:
        error_msg = f"Ошибка: {str(e)}"
        print(error_msg)
        await message.reply_text(error_msg)

    finally:
        # Удаление файла (реализовано в file_manager)
        from utils.file_manager import cleanup
        cleanup(temp_path)