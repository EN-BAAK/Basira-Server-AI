import faiss
import numpy as np
import pickle
from pathlib import Path

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