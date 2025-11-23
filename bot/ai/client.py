import os
import openai

# Получаем ключ из .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class OpenAIClient:
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not set in .env")
        openai.api_key = OPENAI_API_KEY
        self.client = openai
    
    def _ask(self, system_msg: str, user_msg: str, max_tokens: int = 3000, temp: float = 0.7):
        try:
            response = self.client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg}
                ],
                max_tokens=max_tokens,
                temperature=temp
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ AI ошибка: {str(e)}"

# VacancyAnalyzer
class VacancyAnalyzer:
    def __init__(self):
        self.ai = OpenAIClient()
    
    def analyze(self, vacancy_text: str):
        system = "Ты — HR-аналитик. Анализируешь вакансии."
        user = f"Проанализируй вакансию:\n{vacancy_text}\n\nВыдели: должность, требования, ЗП, культуру."
        return self.ai._ask(system, user)