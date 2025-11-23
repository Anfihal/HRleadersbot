# -*- coding: utf-8 -*-
import os
import openai
from dotenv import load_dotenv
import asyncio

# Загружаем переменные окружения
load_dotenv()

async def test_openai_key():
    """Тестирование OpenAI API ключа"""
    print("🔍 Проверка OpenAI API ключа...")
    print("=" * 50)
    
    # Получаем ключ из .env
    api_key = os.getenv("OPENAI_API_KEY")
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key and not openrouter_key:
        print("❌ ОШИБКА: Ни один API ключ не найден в .env файле")
        print("\n💡 Решение:")
        print("1. Добавьте в .env один из ключей:")
        print("   OPENAI_API_KEY=ваш_ключ_openai")
        print("   OPENROUTER_API_KEY=ваш_ключ_openrouter")
        print("2. Получите ключ на platform.openai.com или openrouter.ai")
        return False
    
    # Проверяем OpenAI ключ
    if api_key:
        print(f"🔑 OpenAI ключ найден: {api_key[:10]}...")
        await test_openai_api(api_key, "OpenAI")
    
    # Проверяем OpenRouter ключ
    if openrouter_key:
        print(f"🔑 OpenRouter ключ найден: {openrouter_key[:10]}...")
        await test_openrouter_api(openrouter_key)
    
    return True

async def test_openai_api(api_key: str, provider: str):
    """Тестирование OpenAI API"""
    print(f"\n🔄 Тестируем {provider} API...")
    
    try:
        client = openai.OpenAI(api_key=api_key)
        
        # Простой тестовый запрос
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Скажи 'Тест пройден' на русском"}],
            max_tokens=10
        )
        
        result = response.choices[0].message.content
        print(f"✅ {provider} API работает! Ответ: {result}")
        print(f"🧠 Модель: {response.model}")
        print(f"📊 Использовано токенов: {response.usage.total_tokens}")
        
        return True
        
    except openai.AuthenticationError:
        print(f"❌ {provider}: Неверный API ключ")
        return False
    except openai.RateLimitError:
        print(f"❌ {provider}: Превышен лимит запросов")
        return False
    except openai.APIConnectionError:
        print(f"❌ {provider}: Ошибка подключения к API")
        return False
    except Exception as e:
        print(f"❌ {provider}: Ошибка - {e}")
        return False

async def test_openrouter_api(api_key: str):
    """Тестирование OpenRouter API"""
    print("\n🔄 Тестируем OpenRouter API...")
    
    try:
        client = openai.OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        
        # Тестовый запрос к OpenRouter
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",  # Используем модель через OpenRouter
            messages=[{"role": "user", "content": "Скажи 'OpenRouter тест пройден'"}],
            max_tokens=10
        )
        
        result = response.choices[0].message.content
        print(f"✅ OpenRouter API работает! Ответ: {result}")
        print(f"🧠 Модель: {response.model}")
        print(f"📊 Использовано токенов: {response.usage.total_tokens}")
        
        return True
        
    except Exception as e:
        print(f"❌ OpenRouter: Ошибка - {e}")
        return False

async def check_env_file():
    """Проверка .env файла"""
    print("\n📁 Проверка .env файла...")
    print("=" * 50)
    
    env_path = ".env"
    
    if not os.path.exists(env_path):
        print("❌ Файл .env не найден!")
        print("💡 Создайте файл .env в корне проекта")
        return False
    
    with open(env_path, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
        
        print("📄 Содержимое .env файла:")
        print("-" * 30)
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Маскируем значения для безопасности
                    if 'key' in key.lower() or 'token' in key.lower() or 'secret' in key.lower():
                        masked_value = value[:10] + '...' if len(value) > 10 else '***'
                        print(f"🔐 {key} = {masked_value}")
                    else:
                        print(f"📝 {key} = {value}")
        
        print("-" * 30)
    
    return True

async def main():
    """Основная функция проверки"""
    print("🚀 Запуск проверки API ключей...")
    
    # Проверяем .env файл
    env_ok = await check_env_file()
    if not env_ok:
        return
    
    print("\n" + "=" * 50)
    
    # Проверяем API ключи
    await test_openai_key()
    
    print("\n" + "=" * 50)
    print("🎯 Рекомендации:")
    
    api_key = os.getenv("OPENAI_API_KEY")
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key and not openrouter_key:
        print("❌ Нет рабочих API ключей")
        print("💡 Получите ключ на:")
        print("   - https://platform.openai.com (OpenAI)")
        print("   - https://openrouter.ai (OpenRouter)")
    elif api_key and not openrouter_key:
        print("✅ OpenAI ключ настроен")
        print("💡 Для резерва можно добавить OpenRouter ключ")
    elif openrouter_key and not api_key:
        print("✅ OpenRouter ключ настроен")
        print("💡 OpenRouter обычно дешевле и имеет больше моделей")
    else:
        print("✅ Оба ключа настроены! Отличная работа!")
    
    print("\n🔧 Для HR бота рекомендуется:")
    print("   - OpenRouter (дешевле, больше моделей)")
    print("   - Модель: anthropic/claude-3.5-sonnet")
    print("   - Или: openai/gpt-4o-mini")

if __name__ == "__main__":
    asyncio.run(main())