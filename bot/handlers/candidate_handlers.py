from telegram import Update
from telegram.ext import ContextTypes

from bot.handlers.navigation import go_back_to_main_menu
from bot.utils.keyboards import get_back_keyboard


async def handle_candidate_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка действий соискателя"""
    text = update.message.text.strip()
    
    if text == "📝 Создать резюме":
        await update.message.reply_text(
            "📝 Создание резюме — шаг 1 из 5\n\n"
            "1. Как вас зовут?",
            reply_markup=get_back_keyboard()
        )
        context.user_data['creating_resume'] = True
        context.user_data['resume_step'] = 'name'
        
    elif text == "🤖 Ответить на вопросы":
        await update.message.reply_text(
            "🤖 Подготовка к интервью\n\n"
            "1. Расскажите о себе?\n"
            "(Пишите свободно, я проанализирую)",
            reply_markup=get_back_keyboard()
        )
        context.user_data['interview_mode'] = True
        
    elif text == "🧪 Пройти тест":
        await update.message.reply_text(
            "🧪 Тест по Soft Skills — вопрос 1 из 3\n\n"
            "1. Вы предпочитаете работать в одиночку или в команде?\n"
            "а) Один\nб) С командой\nв) Зависит от задачи",
            reply_markup=get_back_keyboard()
        )
        context.user_data['test_mode'] = True
        context.user_data['test_question'] = 1
        
    elif text == "🎓 Рекомендации курсов":
        await update.message.reply_text(
            "🎓 Рекомендую курсы по вашим навыкам:\n\n"
            "• Python — https://stepik.org/python\n"
            "• HR — https://hr-case.com\n"
            "• Soft Skills — https://praktikum.com/soft\n\n"
            "Хотите подробнее по какому-то курсу?",
            reply_markup=get_back_keyboard()
        )
        
    elif text == "📋 Справки и отпуска":
        keyboard = [
            ["Больничный", "Справка о доходах"],
            ["Отпуск", "⬅️ Назад"]
        ]
        await update.message.reply_text(
            "📋 Выберите документ:",
            reply_markup=keyboard
        )
        context.user_data['document_mode'] = True
        
    elif text == "❓ Помощь":
        await update.message.reply_text(
            "🆘 Справка для соискателя:\n"
            "• Создать резюме — соберу за 5 минут\n"
            "• Ответить на вопросы — подготовка к интервью\n"
            "• Пройти тест — проверим навыки\n"
            "• Рекомендации курсов — подберу обучение\n"
            "• Справки и отпуска — оформлю документы\n\n"
            "Если что-то не работает — /start"
        )
        
    elif text == "🏠 Главное меню":
        await go_back_to_main_menu(update, context)
        
    elif text == "⬅️ Назад":
        await show_candidate_main_menu(update, context)
        
    else:
        await update.message.reply_text("Выберите действие из меню.")


async def show_candidate_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать главное меню соискателя"""
    from bot.handlers.navigation import navigate_to_menu
    await navigate_to_menu(update, context, 'candidate')