# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
import os
import openai

# Получаем ключ из .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class CandidateScorer:
    """Оценка кандидата под вакансию"""
    
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("❌ OPENAI_API_KEY not set in .env")
        openai.api_key = OPENAI_API_KEY
        self.client = openai
    
    def score_match(self, resume: str, vacancy: str):
        """Оценить соответствие"""
        try:
            response = self.client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Ты — эксперт по подбору. Определяешь fit кандидата под вакансию."},
                    {"role": "user", "content": f"""
                        Оцени соответствие кандидата вакансии:

                        Резюме:
                        {resume}

                        Вакансия:
                        {vacancy}

                        Оцени по 10-балльной шкале:
                        • Навыки (0-10)
                        • Опыт (0-10)
                        • Образование (0-10)
                        • Культурный fit (0-10)
                        • Рост (0-10)

                        Итог: средний балл
                        Вердикт: Брать / Не брать / Рассмотреть

                        3 главных плюса и 1 минус.
                    """}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ AI ошибка: {str(e)}"

# Инициализируем AI
scorer = CandidateScorer()

async def handle_find_candidates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка поиска кандидатов"""
    keyboard = [["⬅️ Назад"]]
    await update.message.reply_text(
        "🔍 *AI-поиск кандидатов*\n\n"
        "Пришлите текст вакансии — найду подходящих кандидатов.\n\n"
        "Проанализирую:\n"
        "• Соответствие навыкам\n"
        "• Опыт и образование\n"
        "• Культурный fit\n"
        "• Потенциал роста",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
        parse_mode='Markdown'
    )
    context.user_data['awaiting_vacancy_for_search'] = True

async def process_vacancy_for_search(update: Update, context: ContextTypes.DEFAULT_TYPE, vacancy_text: str):
    """Обработка вакансии для поиска"""
    await update.message.reply_text("🤖 Ищу кандидатов...")
    
    try:
        # Пока заглушка - в реальной версии тут будет поиск по базе
        result = f"""🔍 *Результаты поиска:*

        Найдено 3 подходящих кандидата:

        1. **Иван Петров**
           • Опыт: 5 лет
           • Навыки: Python, Django, PostgreSQL
           • Соответствие: 95%

        2. **Мария Сидорова**
           • Опыт: 3 года
           • Навыки: Python, Flask, MongoDB
           • Соответствие: 88%

        3. **Алексей Кузнецов**
           • Опыт: 4 года
           • Навыки: Python, FastAPI, Redis
           • Соответствие: 82%

        AI анализ: Все кандидаты проходят preliminary screening."""
        
        await update.message.reply_text(result, parse_mode='Markdown')
    except Exception as e:
        result = f"""🔍 *Поиск кандидатов*

        Ищу по базе...

        Найдено: 12 человек
        • Иван — Python, 5 лет
        • Мария — Sales, 3 года
        • Алексей — HR, 4 года

        AI анализ временно недоступен: {str(e)}"""

        await update.message.reply_text(result)
    
    keyboard = [["⬅️ Назад"], ["🔍 Другую вакансию"]]
    await update.message.reply_text(
        "Что дальше?",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    
    context.user_data.pop('awaiting_vacancy_for_search', None)