# -*- coding: utf-8 -*-
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from bot.ai.recruiter.resume_comparator import ResumeComparator

comparator = ResumeComparator()

async def handle_analyze_resumes(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    await update.message.reply_text("🤖 Запускаю AI-анализ...")
    
    result = comparator.compare(resumes_text)
    
    await update.message.reply_text(result, parse_mode='Markdown')
    
    keyboard = [["⬅️ Назад"], ["📊 Сравнить другие"]]
    await update.message.reply_text(
        "Что дальше?",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    
    context.user_data.pop('awaiting_resumes', None)