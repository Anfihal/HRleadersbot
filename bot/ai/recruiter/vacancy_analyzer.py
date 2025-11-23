# -*- coding: utf-8 -*-
import os
import openai

# Получаем ключ из .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class VacancyAnalyzer:
    """Анализ вакансии"""
    
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("❌ OPENAI_API_KEY not set in .env")
        openai.api_key = OPENAI_API_KEY
        self.client = openai
    
    def analyze(self, vacancy_text: str):
        """Проанализировать вакансию"""
        try:
            response = self.client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Ты — HR-аналитик. Анализируешь вакансии и выделяешь ключевое."},
                    {"role": "user", "content": f"""
                        Проанализируй вакансию:

                        {vacancy_text}

                        Выдели:
                        • Должность и уровень
                        • Ключевые требования (хард- и софт-скиллы)
                        • Опыт и образование
                        • Зарплатный диапазон
                        • Культура и условия
                        • Скрытые требования

                        Верни кратко и по пунктам.
                    """}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ AI ошибка: {str(e)}"