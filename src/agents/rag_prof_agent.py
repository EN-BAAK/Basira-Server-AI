
from src.core import rag_prof, prepare_embedding_db

def rag_prof_pipeline(question, pdfs, vector_db, top_k, chunk_size, chunk_overlap):
    db = prepare_embedding_db(vector_db, pdfs, chunk_size, chunk_overlap)
    answer = rag_prof(question, db, top_k)
    return answer