# -*- coding: utf-8 -*-
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from bot.ai.candidate.interview_coach import InterviewCoach

coach = InterviewCoach()

async def handle_interview_prep(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["⬅️ Назад"]]
    await update.message.reply_text(
        "🤖 *AI-подготовка к интервью*\n\n"
        "Пишите ответы на вопросы — я дам профессиональный feedback.\n\n"
        "*Вопросы:*\n"
        "1. Расскажите о себе?\n"
        "2. Почему хотите работать у нас?\n"
        "3. Ваши сильные и слабые стороны?\n"
        "4. Как вы решаете конфликты?\n"
        "5. Где видите себя через 5 лет?",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
        parse_mode='Markdown'
    )
    context.user_data['awaiting_interview_answers'] = True

async def process_interview_answers(update: Update, context: ContextTypes.DEFAULT_TYPE, answers_text: str):
    await update.message.reply_text("🤖 Анализирую ваши ответы...")
    
    position = context.user_data.get('position', 'не указано')
    result = coach.analyze_answers(answers_text, position)
    
    await update.message.reply_text(result, parse_mode='Markdown')
    
    keyboard = [["⬅️ Назад"], ["🤖 Другие вопросы"]]
    await update.message.reply_text(
        "Что дальше?",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    
    context.user_data.pop('awaiting_interview_answers', None)