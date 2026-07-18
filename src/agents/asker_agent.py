from src.core import asker_prepare_embedding_db, asker_questions

def asker_pipeline(question, vector_db, top_k, model):
    db = asker_prepare_embedding_db(vector_db)
    questions = asker_questions(question, db, top_k, model)

    return questions;