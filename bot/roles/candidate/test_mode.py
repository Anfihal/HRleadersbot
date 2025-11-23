# -*- coding: utf-8 -*-
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from bot.ai.candidate.skill_assessment import SkillAssessment

assessor = SkillAssessment()

async def handle_test_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка прохождения теста"""
    keyboard = [["⬅️ Назад"]]
    
    # Генерируем вопросы через AI
    try:
        test_questions = assessor.generate_test_questions("soft_skills")
    except:
        # Резервные вопросы, если AI не доступен
        test_questions = """
1. Вы предпочитаете работать в одиночку или в команде?
а) Один
б) С командой
в) Зависит от задачи

2. Как вы реагируете на критику?
а) Обижаюсь
б) Анализирую
в) Игнорирую

3. Как вы относитесь к изменениям в работе?
а) Сопротивляюсь
б) Принимаю с осторожностью
в) Приветствую

4. Как вы расставляете приоритеты в работе?
а) По срокам
б) По важности
в) По интересу

5. Как вы решаете конфликты?
а) Избегаю
б) Договариваюсь
в) Настаиваю на своём
"""
    
    await update.message.reply_text(
        "🧪 *AI-тест по Soft Skills*\n\n"
        "Ответьте на вопросы — получите профессиональную оценку своих soft skills.\n\n"
        f"{test_questions}\n\n"
        "Пишите ответы (например: 1б, 2б, 3в, 4а, 5б)",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
        parse_mode='Markdown'
    )
    context.user_data['test_mode'] = True

async def process_test_answers(update: Update, context: ContextTypes.DEFAULT_TYPE, answers_text: str):
    """Обработка ответов на тест"""
    await update.message.reply_text("🤖 Анализирую ваши ответы...")
    
    try:
        result = assessor.analyze_soft_skills(answers_text)
        
        await update.message.reply_text(
            "📊 *Результаты теста:*\n\n" + result,
            parse_mode='Markdown'
        )
        
        keyboard = [["⬅️ Назад"], ["🧪 Пройти другой тест"]]
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