# -*- coding: utf-8 -*-
from telegram import ReplyKeyboardMarkup

def get_recruiter_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для рекрутера"""
    keyboard = [
        ["📋 Загрузить вакансию"],
        ["🔍 Найти кандидатов"],
        ["📊 Сравнить резюме"],
        ["📧 Рассылка приглашений"],
        ["❓ Помощь"],
        ["🏠 Главное меню"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_candidate_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для соискателя"""
    keyboard = [
        ["📝 Создать резюме"],
        ["🤖 Ответить на вопросы"],
        ["🧪 Пройти тест"],
        ["🎓 Рекомендации курсов"],
        ["📋 Справки и отпуска"],
        ["❓ Помощь"],
        ["🏠 Главное меню"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_back_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура «Назад»"""
    keyboard = [["⬅️ Назад"]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)