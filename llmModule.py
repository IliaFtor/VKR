import requests

class LLMModule:
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        if not api_key:
            raise ValueError("API ключ не может быть пустым.")
        self.api_key = api_key
        self.model = model
        self.url = "https://bothub.chat/api/v2/openai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Referer": "https://your-site.com"
        }

    def generate_response(self, messages: list, max_tokens: int = 2000) -> str:
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.3
        }
        response = requests.post(self.url, headers=self.headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"] or ""