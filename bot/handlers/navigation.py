# -*- coding: utf-8 -*-
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from bot.utils.keyboards import get_recruiter_keyboard, get_candidate_keyboard


async def navigate_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, role: str):
    """Плавный переход в меню по роли"""
    if role == "recruiter":
        keyboard = get_recruiter_keyboard()
        await update.message.reply_text(
            "🎯 Добро пожаловать, рекрутер!\n\n"
            "Ваше меню:\n"
            "• Загрузить вакансию — добавите новую вакансию для анализа\n"
            "• Найти кандидатов — подберу подходящих по навыкам\n"
            "• Сравнить резюме — помогу выбрать лучшего кандидата\n"
            "• Рассылка приглашений — массовая отправка приглашений\n\n"
            "Выберите действие:",
            reply_markup=keyboard
        )
    elif role == "candidate":
        keyboard = get_candidate_keyboard()
        await update.message.reply_text(
            "🌟 Добро пожаловать, соискатель!\n\n"
            "Ваше меню:\n"
            "• Создать резюме — соберу ваше резюме по вопросам\n"
            "• Ответить на вопросы — подготовка к интервью\n"
            "• Пройти тест — проверим ваши знания\n"
            "• Рекомендации курсов — подберу обучающие курсы\n"
            "• Справки и отпуска — оформлю документы\n\n"
            "Выбирайте, с чего начнём:",
            reply_markup=keyboard
        )
    else:
        await update.message.reply_text("Неизвестная роль. Используйте /start")


async def go_back_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Вернуться в главное меню — чистим состояние и вызываем старт"""
    context.user_data.clear()
    
    # Показываем кнопки выбора роли
    from telegram import KeyboardButton
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