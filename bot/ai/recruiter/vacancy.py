# -*- coding: utf-8 -*-
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from bot.ai.recruiter.vacancy_analyzer import VacancyAnalyzer

analyzer = VacancyAnalyzer()

async def handle_upload_vacancy(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    await update.message.reply_text("🤖 Анализирую вакансию...")
    
    result = analyzer.analyze(vacancy_text)
    
    await update.message.reply_text(result, parse_mode='Markdown')
    
    keyboard = [["⬅️ Назад"], ["📋 Другую вакансию"]]
    await update.message.reply_text(
        "Что дальше?",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    
    context.user_data.pop('awaiting_vacancy', None)