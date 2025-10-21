from llmModule import LLMModule
from config import OPENAI_API_KEY

_llm = None

def get_llm():
    global _llm
    if _llm is None:
        _llm = LLMModule(api_key=OPENAI_API_KEY, model="gpt-4o")
    return _llm

def generate_lecture_summary(text: str) -> str:
    """Генерирует конспект лекции из текста."""
    llm = get_llm()
    messages = [
        {"role": "system", "content": "Ты — эксперт в составлении методических конспектов лекций. На основе распознанного текста создай структурированный, понятный и содержательный конспект."},
        {"role": "user", "content": text}
    ]
    return llm.generate_response(messages, max_tokens=2000)