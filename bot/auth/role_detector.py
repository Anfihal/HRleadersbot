# -*- coding: utf-8 -*-
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from bot.database.user_storage import save_user_role


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start — choose role"""
    user_id = update.effective_user.id
    
    keyboard = [
        [KeyboardButton("👔 Я — Рекрутер")],
        [KeyboardButton("👤 Я — Соискатель")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    
    await update.message.reply_text(
        "Привет! 👋\n\n"
        "Я — HR AI бот. Помогу с подбором и карьерой.\n\n"
        "Кто вы?",
        reply_markup=reply_markup
    )


async def handle_role_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle role choice"""
    user_id = update.effective_user.id
    text = update.message.text.lower()
    
    if "рекрутер" in text or "работодатель" in text:
        # ✅ Сохраняем в БД
        save_user_role(user_id, "recruiter")
        # ✅ Сохраняем в памяти
        context.user_data['role'] = 'recruiter'
        
        keyboard = [
            ["📋 Загрузить вакансию", "🔍 Найти кандидатов"],
            ["📊 Сравнить резюме", "📧 Рассылка приглашений"],
            ["❓ Помощь"]
        ]
        await update.message.reply_text(
            "Отлично! Вы — рекрутер. 🎯\n"
            "Теперь можете:\n"
            "- Загружать вакансии\n"
            "- Искать и анализировать кандидатов\n"
            "- Делать рассылки\n\n"
            "Выберите действие:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
        
    elif "соискатель" in text or "сотрудник" in text:
        # ✅ Сохраняем в БД
        save_user_role(user_id, "candidate")
        # ✅ Сохраняем в памяти
        context.user_data['role'] = 'candidate'
        
        keyboard = [
            ["📝 Создать резюме", "🤖 Ответить на вопросы"],
            ["🧪 Пройти тест", "🎓 Рекомендации курсов"],
            ["📋 Справки и отпуска", "❓ Помощь"]
        ]
        await update.message.reply_text(
            "Привет, кандидат! 🌟\n"
            "Я помогу:\n"
            "- Собрать резюме\n"
            "- Подготовиться к интервью\n"
            "- Пройти тесты\n"
            "- Найти курсы\n\n"
            "Выберите, что нужно:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
    else:
        # Непонятный ввод — просим выбрать по кнопкам
        keyboard = [
            [KeyboardButton("👔 Я — Рекрутер")],
            [KeyboardButton("👤 Я — Соискатель")]
        ]
        await update.message.reply_text(
            "Пожалуйста, выберите роль:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        )