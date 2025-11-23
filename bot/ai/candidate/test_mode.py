# -*- coding: utf-8 -*-
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from bot.ai.candidate.skill_assessment import SkillAssessment

assessor = SkillAssessment()

async def handle_test_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка прохождения testа"""
    keyboard = [["⬅️ Назад"]]
    
    await update.message.reply_text(
        "🧪 *AI-тест по Soft Skills*\n\n"
        "Ответьте на вопросы — получите профессиональную оценку своих soft skills.\n\n"
        "1. Вы предпочитаете работать в одиночку или в команде?\n"
        "2. Как вы реагируете на критику?\n"
        "3. Как вы относитесь к изменениям в работе?\n"
        "4. Как вы расставляете приоритеты в работе?\n"
        "5. Как вы решаете конфликты?\n\n"
        "Пишите ответы (например: 1б, 2б, 3в, 4а, 5б)",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
        parse_mode='Markdown'
    )
    context.user_data['test_mode'] = True

async def process_test_answers(update: Update, context: ContextTypes.DEFAULT_TYPE, answers_text: str):
    """Обработка ответов на test"""
    await update.message.reply_text("🤖 Анализирую ваши ответы...")
    
    try:
        result = assessor.analyze_soft_skills(answers_text)
        
        await update.message.reply_text(
            "📊 *Результаты testа:*\n\n" + result,
            parse_mode='Markdown'
        )
        
        keyboard = [["⬅️ Назад"], ["🧪 Пройти другой test"]]
        await update.message.reply_text(
            "Что дальше?",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
        
    except Exception as e:
        await update.message.reply_text(
            f"⚠️ Ошибка: {str(e)}",
            reply_markup=ReplyKeyboardMarkup([["⬅️ Назад"]], resize_keyboard=True)
        )
    
    context.user_data.pop('test_mode', None)