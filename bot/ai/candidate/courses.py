# -*- coding: utf-8 -*-
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from bot.ai.candidate.course_recommender import CourseRecommender

recommender = CourseRecommender()

async def handle_courses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["⬅️ Назад"]]
    await update.message.reply_text(
        "🎓 *AI-рекомендации курсов*\n\n"
        "Опишите, какие навыки хотите развить:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
        parse_mode='Markdown'
    )
    context.user_data['awaiting_course_request'] = True

async def process_course_request(update: Update, context: ContextTypes.DEFAULT_TYPE, skills_text: str):
    await update.message.reply_text("🤖 Подбираю курсы...")
    
    result = recommender.recommend(skills_text, "beginner")
    
    await update.message.reply_text(result, parse_mode='Markdown')
    
    keyboard = [["⬅️ Назад"], ["🎓 Другие курсы"]]
    await update.message.reply_text(
        "Что дальше?",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    
    context.user_data.pop('awaiting_course_request', None)