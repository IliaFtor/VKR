import os

OPENAI_API_KEY = '' #json web token for bothub.chat
BOT_TOKEN = ""

if not BOT_TOKEN or not OPENAI_API_KEY:
    raise EnvironmentError("Установите BOT_TOKEN и OPENAI_API_KEY в .env или системных переменных")