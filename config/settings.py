# -*- coding: utf-8 -*-
import os

# Переменные из .env
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
DATA_DIR = os.getenv("DATA_DIR", "data")

def validate_settings():
    """Проверка обязательных переменных"""
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")
    return True

# ❌ УБРАТЬ ЭТУ СТРОКУ - не выполняем проверку при импорте
# validate_settings()