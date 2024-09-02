import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.manifold import TSNE   
import matplotlib.pyplot as plt

class Embeddingv2:
    def __init__(self, comments: list[str]):
        # обучение модели
        self.model_name = "intfloat/e5-large-v2"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(self.model_name)

        self.comments = comments
        self.vectors = None # 1024-мерный вектор для комментария
        self.points = None # точки для двумерного пространства, 

    def get_embedding(self, comment):
        inputs = self.tokenizer(comment, return_tensors='pt', truncation=True, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()       

    def get_vectors(self):
        self.vectors = np.array([self.get_embedding(comment) for comment in self.comments])
    
    def get_points(self):
        """Алгоритм t-SNE для отодвигания точек и сокращения вектора."""
        n_samples = self.vectors.shape[0] # проверка на количества образцов комментариев
        perplexity = min(30, n_samples - 1)
        tsne = TSNE(n_components=2, perplexity=perplexity, random_state=42)
        self.points = tsne.fit_transform(self.vectors)

    def convToPoints(vectors: np.array):
        """для независимого метода"""
        n_samples = vectors.shape[0] # проверка на количества образцов комментариев
        perplexity = min(30, n_samples - 1)
        tsne = TSNE(n_components=2, perplexity=perplexity, random_state=42)
        return tsne.fit_transform(vectors)
    