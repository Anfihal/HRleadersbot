# test_imports.py
import sys
import os

# Добавляем корень проекта в sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("🔍 Пошаговая проверка импортов...")

# Шаг 1: bot
try:
    import bot
    print("✅ bot импортируется")
except Exception as e:
    print(f"❌ bot: {e}")
    exit(1)

# Шаг 2: bot.auth
try:
    import bot.auth
    print("✅ bot.auth импортируется")
except Exception as e:
    print(f"❌ bot.auth: {e}")
    exit(1)

# Шаг 3: bot.auth.role_detector
try:
    import bot.auth.role_detector
    print("✅ bot.auth.role_detector импортируется")
except Exception as e:
    print(f"❌ bot.auth.role_detector: {e}")
    exit(1)

# Шаг 4: bot.database
try:
    import bot.database
    print("✅ bot.database импортируется")
except Exception as e:
    print(f"❌ bot.database: {e}")
    exit(1)

# Шаг 5: bot.database.user_storage
try:
    import bot.database.user_storage
    print("✅ bot.database.user_storage импортируется")
except Exception as e:
    print(f"❌ bot.database.user_storage: {e}")
    exit(1)

# Шаг 6: bot.roles
try:
    import bot.roles
    print("✅ bot.roles импортируется")
except Exception as e:
    print(f"❌ bot.roles: {e}")
    exit(1)

# Шаг 7: bot.roles.recruiter
try:
    import bot.roles.recruiter
    print("✅ bot.roles.recruiter импортируется")
except Exception as e:
    print(f"❌ bot.roles.recruiter: {e}")
    exit(1)

# Шаг 8: bot.roles.recruiter.vacancy
try:
    import bot.roles.recruiter.vacancy
    print("✅ bot.roles.recruiter.vacancy импортируется")
except Exception as e:
    print(f"❌ bot.roles.recruiter.vacancy: {e}")
    exit(1)

print("✅ Все импорты прошли!")