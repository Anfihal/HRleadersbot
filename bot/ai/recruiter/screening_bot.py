# -*- coding: utf-8 -*-
from bot.ai.base_client import BaseAIClient

class ScreeningBot(BaseAIClient):
    """Прескрининг кандидатов"""
    
    def screen_answers(self, answers: str, vacancy: str):
        """Проанализировать ответы кандидата"""
        system = "Ты — рекруiter. Оцениваешь кандидата по ответам на вопросы."
        user = f"""
        Проанализируй ответы кандидата:

        Ответы:
        {answers}

        Вакансия:
        {vacancy}

        Оцени:
        • Соответствие опыту
        • Soft skills
        • Мотивация
        • Культурный fit
        • Риски

        Вердикт: Подходит / Не подходит / Рассмотреть
        """
        return self._ask(system, user)