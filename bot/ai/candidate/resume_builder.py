# -*- coding: utf-8 -*-
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from bot.ai.candidate.resume_writer import ResumeWriter

writer = ResumeWriter()

# Состояния
STATE_WAITING_FOR_ANSWERS = "waiting_answers"

# Клавиатуры
def get_back_keyboard():
    """Клавиатура с 'Назад' и 'Главное меню'"""
    return ReplyKeyboardMarkup([
        [KeyboardButton("⬅️ Назад")],
        [KeyboardButton("🏠 Главное меню")]
    ], resize_keyboard=True)

def get_final_keyboard():
    """Клавиатура after завершения"""
    return ReplyKeyboardMarkup([
        [KeyboardButton("📝 Создать новое резюме")],
        [KeyboardButton("🏠 Главное меню")]
    ], resize_keyboard=True)


async def handle_create_resume(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало создания резюме"""
    await update.message.reply_text(
        "📝 *AI-создание резюме* — быстро и профессионально\n\n"
        "Ответьте на вопросы *одним сообщением* через точку с запятой:\n\n"
        "1. *Как вас зовут?*\n"
        "2. *На какую должность претендуете?*\n"
        "3. *Опыт работы (лет)?*\n"
        "4. *Ваши ключевые навыки?*\n"
        "5. *Образование?*\n\n"
        "*Формат:* `Имя; Должность; 5; Навыки; Образование`\n\n"
        "*Пример:* `Иванов Иван; Python разработчик; 5; Python, Django, Git; Высшее, Программирование`",
        reply_markup=get_back_keyboard(),
        parse_mode='Markdown'
    )
    
    context.user_data['state'] = STATE_WAITING_FOR_ANSWERS


async def handle_resume_process(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка процесса создания резюме"""
    text = update.message.text.strip()
    
    # Обработка навигации
    if text == "⬅️ Назад":
        await go_to_main_menu(update, context)
        return
    elif text == "🏠 Главное меню":
        await go_to_main_menu(update, context)
        return
    
    # Определение состояния
    state = context.user_data.get('state')
    
    if state == STATE_WAITING_FOR_ANSWERS:
        await process_resume_answers(update, context, text)


async def process_resume_answers(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    """Обработка ответов пользователя и AI-анализ"""
    await update.message.reply_text("🤖 Обрабатываю ответы...")
    
    try:
        # Разбираем ответы
        parts = [part.strip() for part in text.split(';')]
        
        if len(parts) < 5:
            await update.message.reply_text(
                "❌ Пожалуйста, укажите все данные через точку с запятой.\n\n"
                "Формат: `Имя; Должность; Опыт; Навыки; Образование`",
                reply_markup=get_back_keyboard()
            )
            return
        
        # Извлекаем данные
        name, position, experience, skills, education = parts[:5]
        
        # Валидация опыта
        try:
            exp_num = int(experience.replace(' ', ''))
            if exp_num < 0:
                raise ValueError
        except ValueError:
            await update.message.reply_text(
                "❌ Укажите опыт работы цифрами (например: 5)",
                reply_markup=get_back_keyboard()
            )
            return
        
        # Сохраняем данные
        resume_data = {
            'name': name,
            'position': position,
            'experience': str(exp_num),
            'skills': skills,
            'education': education
        }
        
        # Показываем собранные данные
        collected_info = f"""
✅ *Данные собраны:*

👤 *Имя:* {name}
🎯 *Должность:* {position}
📅 *Опыт:* {exp_num} лет
💡 *Навыки:* {skills}
🎓 *Образование:* {education}
"""
        
        await update.message.reply_text(collected_info, parse_mode='Markdown')
        
        # AI-анализ и улучшение
        await improve_resume(update, context, resume_data)
        
    except Exception as e:
        await update.message.reply_text(
            f"❌ Произошла ошибка: {e}",
            reply_markup=get_back_keyboard()
        )


async def improve_resume(update: Update, context: ContextTypes.DEFAULT_TYPE, resume_data: dict):
    """AI-улучшение резюме"""
    await update.message.reply_text("🤖 Запускаю AI-улучшение...")
    
    try:
        # Формируем текст резюме
        resume_text = f"""
        Имя: {resume_data.get('name', '—')}
        Должность: {resume_data.get('position', '—')}
        Опыт: {resume_data.get('experience', '—')} лет
        Навыки: {resume_data.get('skills', '—')}
        Образование: {resume_data.get('education', '—')}
        """
        
        # AI-улучшение
        improved_resume = writer.improve(resume_text, resume_data.get('position', ''))
        
        # Показываем улучшенное резюме
        await update.message.reply_text(
            "🎉 *AI-улучшение завершено!*\n\n"
            "📄 *Ваше профессиональное резюме:*\n\n" + improved_resume,
            parse_mode='Markdown'
        )
        
        # Предлагаем действия
        await update.message.reply_text(
            "Что дальше?",
            reply_markup=get_final_keyboard()
        )
        
    except Exception as e:
        await update.message.reply_text(
            f"⚠️ AI временно недоступен: {str(e)[:100]}...",
            reply_markup=get_final_keyboard()
        )


async def go_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Переход в главное меню"""
    context.user_data.pop('state', None)
    
    await update.message.reply_text(
        "↩️ Возвращаемся в главное меню...",
        reply_markup=None
    )
    
    # Показываем меню соискателя
    await show_candidate_menu(update, context)


async def show_candidate_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать меню соискателя"""
    keyboard = [
        [KeyboardButton("📝 Создать резюме"), KeyboardButton("🤖 Ответить на вопросы")],
        [KeyboardButton("🧪 Пройти test"), KeyboardButton("🎓 Рекомендации курсов")],
        [KeyboardButton("📋 Справки и отпуска"), KeyboardButton("❓ Помощь")]
    ]
    
    await update.message.reply_text(
        "🌟 *Меню соискателя*\n\nChoose action:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
        parse_mode='Markdown'
    )