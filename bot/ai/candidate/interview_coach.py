# -*- coding: utf-8 -*-
import os
import openai

# Получаем ключ из .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class InterviewCoach:
    """Подготовка к интервью"""
    
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("❌ OPENAI_API_KEY not set in .env")
        openai.api_key = OPENAI_API_KEY
        self.client = openai
    
    def analyze_answers(self, answers: str, role: str):
        """Проанализировать ответы кандидата"""
        try:
            response = self.client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Ты — карьерный коуч. Даёшь feedback по ответам на интервью."},
                    {"role": "user", "content": f"""
                        Проанализируй ответы on типовые вопросы:

                        Ответы:
                        {answers}

                        Должность: {role}

                        Оцени:
                        • Чёткость
                        • Релевантность
                        • Конкретика
                        • Soft skills
                        • Уверенность

                        Дай 3 совета по улучшению.
                    """}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ AI ошибка: {str(e)}"