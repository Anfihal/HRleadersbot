# -*- coding: utf-8 -*-
import os
import openai

# Получаем ключ из .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class ResumeWriter:
    """Улучшение резюме"""
    
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("❌ OPENAI_API_KEY not set in .env")
        openai.api_key = OPENAI_API_KEY
        self.client = openai
    
    def improve(self, resume_text: str, job_title: str = ""):
        """Улучшить резюме"""
        try:
            response = self.client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Ты — эксперт по карьерному консультированию. Улучшаешь резюме, делая их прохожими."},
                    {"role": "user", "content": f"""
                        Улучши резюме для вакансии: {job_title or "не указано"}

                        Резюме:
                        {resume_text}

                        Задачи:
                        1. Сделай профессиональным и цепляющим
                        2. Добавь достижения и метрики
                        3. Усиль ключевые навыки
                        4. Сделай релевантным
                        5. Используй HR-ключевые слова

                        Верни улучшенное резюме.
                    """}
                ],
                max_tokens=3000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ AI ошибка: {str(e)}"