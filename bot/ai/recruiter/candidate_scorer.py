# -*- coding: utf-8 -*-
import os
import openai

# Получаем ключ из .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class CandidateScorer:
    """Оценка кандидата под вакансию"""
    
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("❌ OPENAI_API_KEY not set in .env")
        openai.api_key = OPENAI_API_KEY
        self.client = openai
    
    def score_match(self, resume: str, vacancy: str):
        """Оценить соответствие"""
        try:
            response = self.client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Ты — эксперт по подбору. Определяешь fit кандидата под вакансию."},
                    {"role": "user", "content": f"""
                        Оцени соответствие кандидата вакансии:

                        Резюме:
                        {resume}

                        Вакансия:
                        {vacancy}

                        Оцени по 10-балльной шкале:
                        • Навыки (0-10)
                        • Опыт (0-10)
                        • Образование (0-10)
                        • Культурный fit (0-10)
                        • Рост (0-10)

                        Итог: средний балл
                        Вердикт: Брать / Не брать / Рассмотреть

                        3 главных плюса и 1 минус.
                    """}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ AI ошибка: {str(e)}"