# -*- coding: utf-8 -*-
import os
import openai

# Получаем ключ из .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class ResumeComparator:
    """Сравнение резюме кандидатов"""
    
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("❌ OPENAI_API_KEY not set in .env")
        openai.api_key = OPENAI_API_KEY
        self.client = openai
    
    def compare(self, resumes_text: str):
        """Сравнить резюме"""
        try:
            response = self.client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Ты — топовый HR-директор. Анализируешь резюме и даёшь честную, детальную оценку."},
                    {"role": "user", "content": f"""
                        Проанализируй и сравни резюме кандидатов:

                        {resumes_text}

                        Задачи:
                        1. Краткое резюме каждого (2-3 строки)
                        2. Сравнительная таблица: Навыки | Опыт | Образование | Достижения | Soft Skills
                        3. Рейтинг кандидатов с обоснованием
                        4. Рекомендация: кого брать и почему

                        Говори как профессиональный HR.
                    """}
                ],
                max_tokens=3000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ AI ошибка: {str(e)}"