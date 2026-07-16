from sentence_transformers import SentenceTransformer

class EmbeddingModel:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed_documents(self, texts):
        embeddings = self.model.encode(texts, show_progress_bar=True)
        return embeddings

    def embed_query(self, query):
        embedding = self.model.encode(query)
        return embedding