from config import  models
from src.prompts import QUESTION_BREAKER_PROMPT
from src.services import load_embedding_vector, search_in_vector, clean_asker_output
from src.tools import ghaumah_llm_model_response as llm_model_response

def prepare_embedding_db(vector_db):
    db = load_embedding_vector(vector_db)
    return db

def asker_questions(question, db, top_k, model=models.QweQ):
    context = search_in_vector(question, db, top_k)
    prompt = QUESTION_BREAKER_PROMPT.format(context, question)

    answer = llm_model_response(prompt, model)

    return clean_asker_output(answer);