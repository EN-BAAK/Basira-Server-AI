from langchain_google_genai import ChatGoogleGenerativeAI
from config import models, client, settings

def ghaumah_llm_model_response(prompt, model=models.DeepSeek):
    tokens = settings.MAX_TOKENS if model == models.DeepSeek else 5000

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=tokens,
    )
    return response.choices[0].message.content.strip()

def gemini_llm_model_response(prompt):
    client = ChatGoogleGenerativeAI(
        model=settings.GEMINI_MODEL,
        google_api_key=settings.GEMINI_API_KEY,
        temperature=0.2,
        max_tokens=settings.MAX_TOKENS*10
    )

    response = client.invoke(prompt)
    return response.content