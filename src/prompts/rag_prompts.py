RAG_SYSTEM_PROMPT = "You are a helpful AI assistant. Answer ONLY using the provided context."

RAG_USER_PROMPT_TEMPLATE = """
CONTEXT:
{context}

QUESTION:
{question}

INSTRUCTIONS:
- Answer ONLY using the context above
- If the answer is not in the context, say "I don't know"
- Be precise and technical
"""