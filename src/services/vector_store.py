import faiss
import numpy as np
import pickle
from pathlib import Path
from src.utils import load_all_pdfs, create_chunks
from src.services import EmbeddingModel

class VectorStore:
    def __init__(self, dimension):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.metadata = []

    def add(self, embeddings, documents):
        vectors = np.array(embeddings).astype("float32")
        self.index.add(vectors)
        self.metadata.extend(documents)

    def search(self, query_vector, k=5):
        query = np.array([query_vector]).astype("float32")
        distances, indices = self.index.search(query, k)

        results = []
        for position, idx in enumerate(indices[0]):
            if idx == -1:
                continue

            results.append({
                "score": float(distances[0][position]),
                **self.metadata[idx]
            })
        return results

    def save(self, folder):
        folder = Path(folder)
        folder.mkdir(exist_ok=True)
        faiss.write_index(self.index, str(folder / "index.faiss"))
        with open(folder / "metadata.pkl", "wb") as f:
            pickle.dump(self.metadata, f)

    def load(self, folder):
        folder = Path(folder)
        self.index = faiss.read_index(str(folder / "index.faiss"))
        with open(folder / "metadata.pkl", "rb") as f:
            self.metadata = pickle.load(f)

def build_embedding_vector_store(pdf_folder, vector_db_path, chunk_size, chunk_overlap):
    documents = load_all_pdfs(pdf_folder)
    chunks = create_chunks(
        documents,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
      )

    texts = [c["text"] for c in chunks]

    embedding_model = EmbeddingModel()
    vectors = embedding_model.embed_documents(texts)

    db = VectorStore(dimension=vectors.shape[1])
    db.add(vectors, chunks)
    db.save(vector_db_path)

    return db

def load_embedding_vector(vector_db_path):
    faiss_file = vector_db_path / "index.faiss"
    metadata_file = vector_db_path / "metadata.pkl"

    if faiss_file.exists() and metadata_file.exists():
        db = VectorStore(dimension=0) 
        db.load(vector_db_path)
        return db
    else:
        return False

def search_in_vector(query, db, top_k):
  if not db:
      raise ValueError("Vector database is not built or loaded.")

  embedding_model = EmbeddingModel()
  query_vector =  embedding_model.embed_query(query)

  results = db.search(query_vector, k=top_k)
  context = "\n\n".join([r["text"] for r in results])

  return context