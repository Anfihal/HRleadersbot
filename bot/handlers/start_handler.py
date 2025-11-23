# -*- coding: utf-8 -*-
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes

from bot.database.user_storage import save_user_role
from bot.handlers.navigation import navigate_to_menu


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Старт — выбор роли. Чистим состояние и показываем выбор."""
    # Чистим предыдущее состояние
    context.user_data.clear()
    
    keyboard = [
        [KeyboardButton("👔 Я — Рекрутер / Работодатель")],
        [KeyboardButton("👤 Я — Соискатель / Сотрудник")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    
    await update.message.reply_text(
        "Привет! 👋\n\n"
        "Я — HR AI бот. Помогу с подбором и карьерой.\n\n"
        "Кто вы?",
        reply_markup=reply_markup
    )


async def handle_role_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка выбора роли + плавный переход в профильное меню"""
    user_id = update.effective_user.id
    text = update.message.text.strip().lower()
    
    try:
        if "рекрутер" in text or "работодатель" in text:
            save_user_role(user_id, "recruiter")
            context.user_data['role'] = 'recruiter'
            
            # Плавный переход: сохранение роли → меню рекрутера
            await navigate_to_menu(update, context, 'recruiter')
            
        elif "соискатель" in text or "сотрудник" in text:
            save_user_role(user_id, "candidate")
            context.user_data['role'] = 'candidate'
            
            # Плавный переход: сохранение роли → меню соискателя
            await navigate_to_menu(update, context, 'candidate')
            
        else:
            # Непонятный ввод — вежливо просим выбрать по кнопкам
            keyboard = [
                [KeyboardButton("👔 Я — Рекрутер / Работодатель")],
                [KeyboardButton("👤 Я — Соискатель / Сотрудник")]
            ]
            await update.message.reply_text(
                "Пожалуйста, выберите роль, нажав на кнопку:",
                reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
            )
    except Exception as e:
        await update.message.reply_text(
            "Произошла ошибка. Попробуйте ещё раз. Используйте /start"
        )
        print(f"[ERROR] handle_role_choice: {user_id} — {e}")