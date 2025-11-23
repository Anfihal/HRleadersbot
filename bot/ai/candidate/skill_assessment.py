# -*- coding: utf-8 -*-
import os
import openai

# Получаем ключ из .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class SkillAssessment:
    """Оценка навыков"""
    
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("❌ OPENAI_API_KEY not set in .env")
        openai.api_key = OPENAI_API_KEY
        self.client = openai
    
    def analyze_soft_skills(self, answers: str):
        """Анализ soft skills"""
        try:
            response = self.client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Ты — psychologist и карьерный коуч. Анализируешь soft skills."},
                    {"role": "user", "content": f"""
                        Проанализируй soft skills по ответам:

                        {answers}

                        Оцени по 5-балльной шкале:
                        • Коммуникабельность
                        • Стрессоустойчивость
                        • Лидерство
                        • Работа в команде
                        • Адаптивность
                        • Ответственность

                        Комментарии к каждой.
                    """}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ AI ошибка: {str(e)}"