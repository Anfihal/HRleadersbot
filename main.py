# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import ReplyKeyboardMarkup, KeyboardButton

# Грузим .env
load_dotenv()

# Токен
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    print("❌ TELEGRAM_BOT_TOKEN not found in .env")
    exit(1)

# Инициализация БД
from bot.database.user_storage import init_db
init_db()

# Создаём приложение
app = Application.builder().token(TOKEN).build()

# Импортируем старт
from bot.auth.role_detector import start_command

# === Клавиатуры (выносим в константы, чтобы не дублировать) ===
BACK_KEYBOARD = ReplyKeyboardMarkup([
    [KeyboardButton("⬅️ Назад")],
    [KeyboardButton("🏠 Главное меню")]
], resize_keyboard=True)

MAIN_MENU_KEYBOARD = ReplyKeyboardMarkup([
    [KeyboardButton("👔 Я — Рекрутер")],
    [KeyboardButton("👤 Я — Соискатель")]
], resize_keyboard=True, one_time_keyboard=True)

FINAL_KEYBOARD = ReplyKeyboardMarkup([
    [KeyboardButton("📝 Создать новое резюме")],
    [KeyboardButton("🏠 Главное меню")]
], resize_keyboard=True)

RECRUITER_KEYBOARD = ReplyKeyboardMarkup([
    ["📋 Загрузить вакансию", "🔍 Найти кандидатов"],
    ["📊 Сравнить резюме", "📧 Рассылка приглашений"],
    ["❓ Помощь"]
], resize_keyboard=True)

CANDIDATE_KEYBOARD = ReplyKeyboardMarkup([
    ["📝 Создать резюме", "🤖 Ответить на вопросы"],
    ["🧪 Пройти тест", "🎓 Рекомендации курсов"],
    ["📋 Справки и отпуска", "❓ Помощь"]
], resize_keyboard=True)

# === Обработчик сообщений ===
async def handle_message(update, context):
    text = update.message.text.strip()
    
    # Универсальные кнопки — в приоритете
    if text == "🏠 Главное меню":
        await go_to_main_menu(update, context)
        return
    elif text == "⬅️ Назад":
        await go_back(update, context)
        return
    
    # === AI-состояния ===
    
    # Если ждём резюме для сравнения
    if context.user_data.get('awaiting_resumes'):
        try:
            from bot.roles.recruiter.analyze import process_resumes_for_comparison
            await process_resumes_for_comparison(update, context, text)
            return
        except Exception as e:
            await update.message.reply_text(f"⚠️ Ошибка анализа резюме: {e}")
            context.user_data.pop('awaiting_resumes', None)
    
    # Если ждём вакансию для анализа
    if context.user_data.get('awaiting_vacancy'):
        try:
            from bot.roles.recruiter.vacancy import process_vacancy_text
            await process_vacancy_text(update, context, text)
            return
        except Exception as e:
            await update.message.reply_text(f"⚠️ Ошибка обработки вакансии: {e}")
            context.user_data.pop('awaiting_vacancy', None)
    
    # Если ждём вакансию для поиска
    if context.user_data.get('awaiting_vacancy_for_search'):
        try:
            from bot.roles.recruiter.search import process_vacancy_for_search
            await process_vacancy_for_search(update, context, text)
            return
        except Exception as e:
            await update.message.reply_text(f"⚠️ Ошибка поиска: {e}")
            context.user_data.pop('awaiting_vacancy_for_search', None)
    
    # Если ждём ответы на интервью
    if context.user_data.get('awaiting_interview_answers'):
        try:
            from bot.roles.candidate.answer_helper import process_interview_answers
            await process_interview_answers(update, context, text)
            return
        except Exception as e:
            await update.message.reply_text(f"⚠️ Ошибка обработки ответов: {e}")
            context.user_data.pop('awaiting_interview_answers', None)
    
    # Если ждём ответы на тест
    if context.user_data.get('test_mode'):
        try:
            from bot.roles.candidate.test_mode import process_test_answers
            await process_test_answers(update, context, text)
            return
        except Exception as e:
            await update.message.reply_text(f"⚠️ Ошибка теста: {e}")
            context.user_data.pop('test_mode', None)
    
    # Если ждём запрос на курсы
    if context.user_data.get('awaiting_course_request'):
        try:
            from bot.roles.candidate.courses import process_course_request
            await process_course_request(update, context, text)
            return
        except Exception as e:
            await update.message.reply_text(f"⚠️ Ошибка курсов: {e}")
            context.user_data.pop('awaiting_course_request', None)
    
    # Если нет роли — выбор роли
    if 'role' not in context.user_data:
        try:
            from bot.auth.role_detector import handle_role_choice
            await handle_role_choice(update, context)
            return
        except Exception as e:
            await update.message.reply_text(f"⚠️ Ошибка выбора роли: {e}")
    
    # Если в процессе создания резюме
    if context.user_data.get('state') in ['waiting_answers', 'asking_details']:
        try:
            from bot.roles.candidate.resume_builder import handle_resume_process
            await handle_resume_process(update, context)
            return
        except Exception as e:
            await update.message.reply_text(f"⚠️ Ошибка создания резюме: {e}")
            context.user_data.pop('state', None)
    
    # Роутим по роли
    role = context.user_data.get('role')
    if role == "recruiter":
        await handle_recruiter_action(update, context, text)
    elif role == "candidate":
        await handle_candidate_action(update, context, text)
    else:
        await update.message.reply_text("❌ Ошибка роли. Use /start")

# === Универсальные функции навигации ===
async def go_to_main_menu(update, context):
    """Переход в главное меню"""
    context.user_data.clear()
    await update.message.reply_text(
        "🔄 Возвращаемся к выбору роли...",
        reply_markup=None
    )
    await start_command(update, context)

async def go_back(update, context):
    """Возврат назад"""
    # Сбрасываем все возможные состояния
    states_to_clear = [
        'awaiting_resumes', 'awaiting_vacancy', 'awaiting_vacancy_for_search',
        'awaiting_interview_answers', 'test_mode', 'awaiting_course_request', 'state'
    ]
    
    for state in states_to_clear:
        context.user_data.pop(state, None)
    
    role = context.user_data.get('role')
    if role == "recruiter":
        await show_recruiter_menu(update, context)
    elif role == "candidate":
        await show_candidate_menu(update, context)
    else:
        await update.message.reply_text("❌ Неизвестная роль. Use /start")

# === Роутинг для рекрутера ===
async def handle_recruiter_action(update, context, text):
    if text == "📋 Загрузить вакансию":
        try:
            from bot.roles.recruiter.vacancy import handle_upload_vacancy
            await handle_upload_vacancy(update, context)
        except Exception as e:
            await update.message.reply_text(f"⚠️ Ошибка: {e}", reply_markup=BACK_KEYBOARD)
    
    elif text == "🔍 Найти кандидатов":
        try:
            from bot.roles.recruiter.search import handle_find_candidates
            await handle_find_candidates(update, context)
        except Exception as e:
            await update.message.reply_text(f"⚠️ Ошибка: {e}", reply_markup=BACK_KEYBOARD)
    
    elif text == "📊 Сравнить резюме":
        try:
            from bot.roles.recruiter.analyze import handle_analyze_resumes
            await handle_analyze_resumes(update, context)
        except Exception as e:
            await update.message.reply_text(f"⚠️ Ошибка: {e}", reply_markup=BACK_KEYBOARD)
    
    elif text == "📧 Рассылка приглашений":
        try:
            from bot.roles.recruiter.invite import handle_invite_mailing
            await handle_invite_mailing(update, context)
        except Exception as e:
            await update.message.reply_text(f"⚠️ Ошибка: {e}", reply_markup=BACK_KEYBOARD)
    
    elif text == "❓ Помощь":
        await update.message.reply_text(
            "🆘 *Справка для рекрутера:*\n"
            "• Загрузить вакансию — добавьте вакансию, я проанализирую\n"
            "• Найти кандидатов — укажу подходящих по навыкам\n"
            "• Сравнить резюме — помогу выбрать лучшего\n"
            "• Рассылка — mass invitations",
            reply_markup=BACK_KEYBOARD,
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            "❌ Выберите действие из меню.",
            reply_markup=BACK_KEYBOARD
        )

# === Роутинг для соискателя ===
async def handle_candidate_action(update, context, text):
    if text in ["📝 Создать резюме", "📝 Создать новое резюме"]:
        try:
            from bot.roles.candidate.resume_builder import handle_create_resume
            await handle_create_resume(update, context)
        except Exception as e:
            await update.message.reply_text(f"⚠️ Ошибка: {e}", reply_markup=BACK_KEYBOARD)
    
    elif text == "🤖 Ответить на вопросы":
        try:
            from bot.roles.candidate.answer_helper import handle_interview_prep
            await handle_interview_prep(update, context)
        except Exception as e:
            await update.message.reply_text(f"⚠️ Ошибка: {e}", reply_markup=BACK_KEYBOARD)
    
    elif text == "🧪 Пройти тест":
        try:
            from bot.roles.candidate.test_mode import handle_test_mode
            await handle_test_mode(update, context)
        except Exception as e:
            await update.message.reply_text(f"⚠️ Ошибка: {e}", reply_markup=BACK_KEYBOARD)
    
    elif text == "🎓 Рекомендации курсов":
        try:
            from bot.roles.candidate.courses import handle_courses
            await handle_courses(update, context)
        except Exception as e:
            await update.message.reply_text(f"⚠️ Ошибка: {e}", reply_markup=BACK_KEYBOARD)
    
    elif text == "📋 Справки и отпуска":
        await update.message.reply_text(
            "📋 *Справки и отпуска*\n\n"
            "• Больничный — 3 дня\n"
            "• Справка о доходах — 1 день\n"
            "• Отпуск — 7 дней\n\n"
            "⚠️ Пока без автоматизации",
            reply_markup=BACK_KEYBOARD,
            parse_mode='Markdown'
        )
    
    elif text == "❓ Помощь":
        await update.message.reply_text(
            "🆘 *Справка для соискателя:*\n"
            "• Создать резюме — соберу за 5 минут\n"
            "• Ответить на вопросы — подготовка к интервью\n"
            "• Пройти тест — проверим навыки\n"
            "• Рекомендации курсов — подберу обучение\n"
            "• Справки и отпуска — оформлю документы",
            reply_markup=BACK_KEYBOARD,
            parse_mode='Markdown'
        )
    
    else:
        await update.message.reply_text(
            "❌ Выберите действие из меню.",
            reply_markup=BACK_KEYBOARD
        )

# === Показать меню ===
async def show_recruiter_menu(update, context):
    """Показать меню рекрутера"""
    await update.message.reply_text(
        "🎯 *Меню рекрутера*\n\nChoose action:",
        reply_markup=RECRUITER_KEYBOARD,
        parse_mode='Markdown'
    )

async def show_candidate_menu(update, context):
    """Показать меню соискателя"""
    await update.message.reply_text(
        "🌟 *Меню соискателя*\n\nChoose action:",
        reply_markup=CANDIDATE_KEYBOARD,
        parse_mode='Markdown'
    )

# === Регистрируем хендлеры ===
app.add_handler(CommandHandler("start", start_command))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# === Запуск ===
if __name__ == "__main__":
    print("🤖 HR AI Bot started...")
    app.run_polling()