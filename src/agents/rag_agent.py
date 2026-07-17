from src.core import RAG

def rag_pipeline(question, pdfs, vector_db):
  rag = RAG(
    pdf_folder=pdfs,
    chunk_overlap=50,
    chunk_size=500,
    top_k=3,
    vector_db_path=vector_db
  )

  rag.load()

  answer = rag.ask(question)
  return answer