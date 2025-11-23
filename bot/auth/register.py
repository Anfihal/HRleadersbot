import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Загружаем .env
load_dotenv()

# Токен из .env
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    print("❌ BOT_TOKEN не найден в .env")
    exit(1)

# Инициализация БД
from bot.database.user_storage import init_db
init_db()

# Создаём приложение
application = Application.builder().token(TOKEN).build()


def main():
    """Запуск бота"""
    # Регистрируем /start
    from bot.auth.role_detector import start_command
    application.add_handler(CommandHandler("start", start_command))
    
    # Регистрируем общий текст
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Запускаем
    print("🤖 HR AI Бот запущен...")
    application.run_polling()


async def handle_message(update, context):
    """Центральный обработчик текста"""
    text = update.message.text.strip().lower()
    
    # Если нет роли — обрабатываем выбор роли
    if 'role' not in context.user_data:
        from bot.auth.role_detector import handle_role_choice
        await handle_role_choice(update, context)
        return
    
    # Иначе — показываем, что в меню
    role = context.user_data.get('role')
    
    if role == "recruiter":
        await update.message.reply_text(
            "🎯 Вы — рекрутер. Используйте кнопки меню:\n"
            "• Загрузить вакансию\n"
            "• Найти кандидатов\n"
            "• Сравнить резюме\n"
            "• Рассылка приглашений\n"
            "• Помощь",
            reply_markup=None
        )
    elif role == "candidate":
        await update.message.reply_text(
            "🌟 Вы — соискатель. Используйте кнопки меню:\n"
            "• Создать резюме\n"
            "• Ответить на вопросы\n"
            "• Пройти тест\n"
            "• Рекомендации курсов\n"
            "• Справки и отпуска\n"
            "• Помощь",
            reply_markup=None
        )
    else:
        await update.message.reply_text("Ошибка роли. Используйте /start")


if __name__ == "__main__":
    main()
   