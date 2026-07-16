from langchain_google_genai import ChatGoogleGenerativeAI
from config.config import settings 

class LLM:
    def __init__(self, model=None):
        self.model_name = model or settings.GEMINI_MODEL
        
        self.client = ChatGoogleGenerativeAI(
            model=self.model_name,
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0.2,
            max_tokens=500
        )

    def generate(self, prompt):
        messages = [
            (
                "system",
                "You are a helpful AI assistant. Answer ONLY using the provided context."
            ),
            (
                "user", 
                prompt
            ),
        ]
        response = self.client.invoke(messages)
        return response.content