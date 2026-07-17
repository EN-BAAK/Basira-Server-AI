from sentence_transformers import SentenceTransformer
from config import settings

class EmbeddingModel:
    def __init__(self):
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL)

    def embed_documents(self, texts):
        embeddings = self.model.encode(texts, show_progress_bar=True)
        return embeddings

    def embed_query(self, query):
        embedding = self.model.encode(query)
        return embedding