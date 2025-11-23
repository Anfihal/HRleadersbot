from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from bot.ai.candidate.resume_writer import ResumeWriter
from bot.database.user_storage import update_user_data
import json
import logging

logger = logging.getLogger(__name__)

# Состояния
STATE_WAITING_FOR_ANSWERS = "waiting_answers"

# Клавиатуры
BACK_KEYBOARD = ReplyKeyboardMarkup([
    [KeyboardButton("⬅️ Назад")],
    [KeyboardButton("🏠 Главное меню")]
], resize_keyboard=True)

FINAL_KEYBOARD = ReplyKeyboardMarkup([
    [KeyboardButton("📝 Создать новое резюме")],
    [KeyboardButton("🏠 Главное меню")]
], resize_keyboard=True)

writer = ResumeWriter()

async def handle_create_resume(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало создания резюме с AI"""
    await update.message.reply_text(
        "📝 *AI-создание резюме* — профессионально и быстро\n\n"
        "Ответьте на вопросы *одним сообщением* через точку с запятой:\n\n"
        "1. *Как вас зовут?*\n"
        "2. *На какую должность претендуете?*\n"
        "3. *Опыт работы (лет)?*\n"
        "4. *Ваши ключевые навыки?*\n"
        "5. *Образование?*\n\n"
        "*Формат:* `Имя; Должность; 5; Навыки; Образование`\n\n"
        "*Пример:* `Иванов Иван; Python разработчик; 5; Python, Django, Git; Высшее, Программирование`",
        reply_markup=BACK_KEYBOARD,
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
    if context.user_data.get('state') == STATE_WAITING_FOR_ANSWERS:
        await process_resume_answers(update, context, text)

async def process_resume_answers(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    """Обработка ответов пользователя и AI-улучшение"""
    await update.message.reply_text("🤖 Обрабатываю ответы...")
    
    try:
        # Разбираем ответы
        parts = [part.strip() for part in text.split(';')]
        
        if len(parts) < 5:
            await update.message.reply_text(
                "❌ Пожалуйста, укажите все данные через точку с запятой.\n\n"
                "Формат: `Имя; Должность; Опыт; Навыки; Образование`",
                reply_markup=BACK_KEYBOARD
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
                reply_markup=BACK_KEYBOARD
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
        
        # Формируем исходное резюме
        original_resume = f"""
        Резюме кандидата

        Имя: {name}
        Должность: {position}
        Опыт: {exp_num} лет
        Навыки: {skills}
        Образование: {education}
        """
        
        # AI-улучшение
        await update.message.reply_text("🤖 Запускаю AI-улучшение...")
        improved_resume = writer.improve(original_resume, position)
        
        # Сохраняем в БД
        await save_resume_to_db(update, resume_data, improved_resume)
        
        # Показываем результат
        await update.message.reply_text(
            "🎉 *AI-резюме готово!*\n\n"
            "📄 *Ваше профессиональное резюме:*\n\n" + improved_resume,
            parse_mode='Markdown'
        )
        
        # Предлагаем действия
        await update.message.reply_text(
            "Что дальше?",
            reply_markup=FINAL_KEYBOARD
        )
        
    except Exception as e:
        logger.error(f"Ошибка обработки ответов: {e}")
        await update.message.reply_text(
            "❌ Произошла ошибка. Попробуйте еще раз.",
            reply_markup=BACK_KEYBOARD
        )

async def save_resume_to_db(update: Update, original_data: dict, improved_resume: str):
    """Сохранение резюме в БД"""
    try:
        user_id = update.effective_user.id
        resume_record = {
            "original": original_data,
            "improved": improved_resume,
            "timestamp": None
        }
        resume_json = json.dumps(resume_record, ensure_ascii=False, indent=2)
        update_user_data(user_id, "resume", resume_json)
        logger.info(f"Резюме сохранено для пользователя {user_id}")
    except Exception as e:
        logger.error(f"Ошибка сохранения в БД: {e}")

async def go_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Переход в главное меню"""
    context.user_data.pop('state', None)
    
    await update.message.reply_text(
        "↩️ Возвращаемся в главное меню...",
        reply_markup=None
    )
    
    # Показываем меню соискателя
    keyboard = ReplyKeyboardMarkup([
        [KeyboardButton("📝 Создать резюме"), KeyboardButton("🤖 Ответить на вопросы")],
        [KeyboardButton("🧪 Пройти тест"), KeyboardButton("🎓 Рекомендации курсов")],
        [KeyboardButton("📋 Справки и отпуска"), KeyboardButton("❓ Помощь")]
    ], resize_keyboard=True)
    
    await update.message.reply_text(
        "🌟 *Меню соискателя*\n\nChoose action:",
        reply_markup=keyboard,
        parse_mode='Markdown'
    )