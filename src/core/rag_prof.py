from src.services import LLM, search_in_vector
from src.prompts import RAG_USER_PROMPT_TEMPLATE

def rag_prof(question, db, top_k):
    context = search_in_vector(question, db, top_k)
    prompt = RAG_USER_PROMPT_TEMPLATE.format(context=context, question=question)

    llm = LLM()
    answer = llm.generate(prompt)
    return answer;
