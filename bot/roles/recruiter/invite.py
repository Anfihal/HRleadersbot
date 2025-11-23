# -*- coding: utf-8 -*-
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

async def handle_invite_mailing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка рассылки приглашений"""
    keyboard = [["⬅️ Назад"]]
    await update.message.reply_text(
        "📧 *Рассылка приглашений*\n\n"
        "Введите ID кандидатов и текст приглашения.\n\n"
        "⚠️ Пока без AI-рассылки",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    context.user_data['awaiting_mailing'] = True