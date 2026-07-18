from src.services import  search_in_vector
from src.prompts import RAG_USER_PROMPT_TEMPLATE
from src.tools import gemini_llm_model_response as llm_model_response
from src.services import load_embedding_vector, build_embedding_vector_store
from pathlib import Path

def rag_prof(question, db, top_k):
    context = search_in_vector(question, db, top_k)
    prompt = RAG_USER_PROMPT_TEMPLATE.format(context=context, question=question)

    answer = llm_model_response(prompt)
    return answer;

def prepare_embedding_db(vector_db, pdfs, chunk_size, chunk_overlap):
    db_path = Path(vector_db)
    faiss_file = db_path / "index.faiss"
    metadata_file = db_path / "metadata.pkl"

    files_exist = faiss_file.exists() and metadata_file.exists()
    
    if files_exist and faiss_file.stat().st_size > 0 and metadata_file.stat().st_size > 0:
        print("Vectors have been found")
    else:
        print("❌Vectors Database is not found")
        build_embedding_vector_store(pdfs, vector_db, chunk_size, chunk_overlap)

    db = load_embedding_vector(vector_db)

    return db;