# -*- coding: utf-8 -*-
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from bot.ai.recruiter.candidate_scorer import CandidateScorer

scorer = CandidateScorer()

async def handle_find_candidates(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    await update.message.reply_text("🤖 Ищу кандидатов...")
    
    # Пока заглушка
    result = f"""🔍 *Результаты поиска:*

    К сожалению, AI временно недоступен.

    Пример результата:
    • Иван — Python разработчик, 5 лет опыта
    • Мария — Frontend, 3 года, React/Vue
    • Алексей — DevOps, 4 года, Docker/K8s

    AI анализ временно недоступен."""

    await update.message.reply_text(result, parse_mode='Markdown')
    
    keyboard = [["⬅️ Назад"], ["🔍 Другую вакансию"]]
    await update.message.reply_text(
        "Что дальше?",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    
    context.user_data.pop('awaiting_vacancy_for_search', None)