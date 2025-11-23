# -*- coding: utf-8 -*-
import os
import openai

# Получаем ключ из .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class CourseRecommender:
    """Рекомендация курсов"""
    
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("❌ OPENAI_API_KEY not set in .env")
        openai.api_key = OPENAI_API_KEY
        self.client = openai
    
    def recommend(self, skills: str, level: str = "beginner"):
        """Подобрать курсы"""
        try:
            response = self.client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Ты — career advisor. Подбираешь ideal курсы для развития."},
                    {"role": "user", "content": f"""
                        Подбери курсы:

                        Навыки: {skills}
                        Уровень: {level}

                        Предложи 5 курсов:
                        • Название
                        • Платформа
                        • Срок
                        • Стоимость
                        • Для кого

                        Сделай релевантным рынку труда.
                    """}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ AI ошибка: {str(e)}"