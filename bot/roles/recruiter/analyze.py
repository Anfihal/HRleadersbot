# -*- coding: utf-8 -*-
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
import os
import openai

# Получаем ключ из .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class ResumeComparator:
    """Сравнение резюме кандидатов"""
    
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("❌ OPENAI_API_KEY not set in .env")
        openai.api_key = OPENAI_API_KEY
        self.client = openai
    
    def compare(self, resumes_text: str):
        """Сравнить резюме"""
        try:
            response = self.client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Ты — топовый HR-директор. Анализируешь резюме и даёшь честную, детальную оценку."},
                    {"role": "user", "content": f"""
                        Проанализируй and сравни резюме кандидатов:

                        {resumes_text}

                        Задачи:
                        1. Краткое резюме каждого (2-3 строки)
                        2. Сравнительная таблица: Навыки | Опыт | Образование | Достижения | Soft Skills
                        3. Рейтинг кандидатов с обоснованием
                        4. Рекомендация: кого брать и почему

                        Говори как профессиональный HR.
                    """}
                ],
                max_tokens=3000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ AI ошибка: {str(e)}"

# Инициализируем AI
comparator = ResumeComparator()

async def handle_analyze_resumes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка анализа резюме"""
    keyboard = [["⬅️ Назад"]]
    await update.message.reply_text(
        "📊 *AI-сравнение резюме*\n\n"
        "Пришлите 2–3 резюме.\n\n"
        "Получите:\n"
        "• Сравнительную таблицу\n"
        "• Рейтинг кандидатов\n"
        "• Рекомендацию с обоснованием\n\n"
        "*Формат:* просто пришлите текстом, разделяя резюме\n"
        "```\n———\n———\n```",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
        parse_mode='Markdown'
    )
    context.user_data['awaiting_resumes'] = True

async def process_resumes_for_comparison(update: Update, context: ContextTypes.DEFAULT_TYPE, resumes_text: str):
    """Обработка присланных резюме"""
    await update.message.reply_text("🤖 Запускаю AI-анализ...")
    
    try:
        result = comparator.compare(resumes_text)
        await update.message.reply_text(result, parse_mode='Markdown')
    except Exception as e:
        result = f"""📊 *Результат анализа:*

    К сожалению, AI временно недоступен.

    Пример результата:
    • Кандидат А: опыт 5 лет, Python, Django
    • Кандидат Б: опыт 3 года, Python, FastAPI
    • Рекомендация: Кандидат А — сильнее технически

    AI ошибка: {str(e)}"""

        await update.message.reply_text(result)
    
    keyboard = [["⬅️ Назад"], ["📊 Сравнить другие"]]
    await update.message.reply_text(
        "Что дальше?",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    
    context.user_data.pop('awaiting_resumes', None)