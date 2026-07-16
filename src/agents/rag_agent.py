from pathlib import Path
from src.services import VectorStore, LLM, EmbeddingModel
from src.utils import load_all_pdfs, create_chunks
from src.prompts import RAG_USER_PROMPT_TEMPLATE

class RAGPipeline:
    def __init__(self, pdf_folder, chunk_size=500, chunk_overlap=50, vector_db_path=None, top_k=4):
        self.pdf_folder = pdf_folder
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        self.vector_db_path = Path(vector_db_path)
        self.top_k = top_k

        self.db = None
        self.embedding_model = EmbeddingModel()
        self.llm = LLM()

    def build(self):
        documents = load_all_pdfs(self.pdf_folder)
        chunks = create_chunks(
            documents,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )

        texts = [c["text"] for c in chunks]
        vectors = self.embedding_model.embed_documents(texts)
        print("vectors", vectors)
        db = VectorStore(dimension=vectors.shape[1])
        db.add(vectors, chunks)
        db.save(self.vector_db_path)
        self.db = db

    def load(self):
        faiss_file = self.vector_db_path / "index.faiss"
        metadata_file = self.vector_db_path / "metadata.pkl"

        if faiss_file.exists() and metadata_file.exists():
            print(f"Loading existing vector database from {self.vector_db_path}...")
            db = VectorStore(dimension=0) 
            db.load(self.vector_db_path)
            self.db = db
            return True
        else:
            print("No existing vector database found.")
            return False

    def ask(self, question):
        if not self.db:
            if not self.load():
                raise ValueError("Vector database is not built or loaded.")

        query_vector = self.embedding_model.embed_query(question)
        results = self.db.search(query_vector, k=self.top_k)

        context = "\n\n".join([r["text"] for r in results])
        
        prompt = RAG_USER_PROMPT_TEMPLATE.format(context=context, question=question)

        print("Context retrieved:", context)
        answer = self.llm.generate(prompt)
        return answer