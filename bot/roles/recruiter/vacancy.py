# -*- coding: utf-8 -*-
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
import os
import openai

# Получаем ключ из .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class VacancyAnalyzer:
    """Анализ вакансии"""
    
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("❌ OPENAI_API_KEY not set in .env")
        openai.api_key = OPENAI_API_KEY
        self.client = openai
    
    def analyze(self, vacancy_text: str):
        """Проанализировать вакансию"""
        try:
            response = self.client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Ты — HR-аналитик. Анализируешь вакансии и выделяешь ключевое."},
                    {"role": "user", "content": f"""
                        Проанализируй вакансию:

                        {vacancy_text}

                        Выдели:
                        • Должность и уровень
                        • Ключевые требования (хард- и софт-скиллы)
                        • Опыт и образование
                        • Зарплатный диапазон
                        • Культура and условия
                        • Скрытые требования

                        Верни кратко и по пунктам.
                    """}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ AI ошибка: {str(e)}"

# Инициализируем AI
analyzer = VacancyAnalyzer()

async def handle_upload_vacancy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка загрузки вакансии"""
    keyboard = [["⬅️ Назад"]]
    await update.message.reply_text(
        "📋 *AI-анализ вакансии*\n\n"
        "Пришлите текст вакансии.\n\n"
        "Получите:\n"
        "• Анализ требований\n"
        "• Оценку ЗП\n"
        "• Рекомендации по улучшению\n"
        "• Ключевые навыки\n\n"
        "*Пример:*\n"
        "```\n"
        "Должность: Менеджер по продажам\n"
        "Требования: опыт от 2 лет, знание CRM\n"
        "ЗП: 100–150k\n"
        "```",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
        parse_mode='Markdown'
    )
    context.user_data['awaiting_vacancy'] = True

async def process_vacancy_text(update: Update, context: ContextTypes.DEFAULT_TYPE, vacancy_text: str):
    """Обработка текста вакансии"""
    await update.message.reply_text("🤖 Анализирую вакансию...")
    
    try:
        result = analyzer.analyze(vacancy_text)
        await update.message.reply_text(result, parse_mode='Markdown')
    except Exception as e:
        result = f"""📋 *Анализ вакансии:*

    Должность: не указано
    Требования: не указаны
    ЗП: не указана

    Рекомендации:
    • Уточните требования
    • Укажите ЗП-диапазон
    • Добавьте описание компании

    AI анализ временно недоступен: {str(e)}"""

        await update.message.reply_text(result)
    
    keyboard = [["⬅️ Назад"], ["📋 Другую вакансию"]]
    await update.message.reply_text(
        "Что дальше?",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    
    context.user_data.pop('awaiting_vacancy', None)