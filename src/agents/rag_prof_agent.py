from pathlib import Path
from src.core import rag_prof
from src.services import load_embedding_vector, build_embedding_vector_store

def rag_prof_pipeline(question, pdfs, vector_db, top_k, chunk_size, chunk_overlap):
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

    answer = rag_prof(question, db, top_k)
    return answer