from gensim.models import Word2Vec
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

from nltk import word_tokenize
import numpy as np

class Embedding:
    def __init__(self, comments: list[str], 
                 vSize: int = 100, window: int = 10, 
                 minCountWord: int = 1, workers: int = 4) -> None:
        """
        Иницилизация настроек модели
        """
        self.vSize = vSize # размер вектора
        self.window = window
        self.minCountWord = minCountWord # минимальное количество вхождения для слова
        self.workers = workers
        self.comments = comments
        self.vectors = None # векторы комментариев
        # токенизация комментария
        tagged_data = [TaggedDocument(words=self.tokenize(comment),
                                      tags=[str(i)]) for i, comment in enumerate(self.comments)]
        
        self.model = Doc2Vec(vector_size=vSize,
                             window=window,
                             min_count=minCountWord,
                             workers=workers)
        # словарь
        self.model.build_vocab(tagged_data)
        # обучение модели
        self.model.train(tagged_data, total_examples=self.model.corpus_count, epochs=10)

    def tokenize(self, comment: str):
        """Токенизация комментария"""
        return word_tokenize(comment.lower())

    def get_vector(self, comment: str):
        """"Возвращает векторное представление комментария на обученной модели"""
        tokens = self.tokenize(comment)
        return self.model.infer_vector(tokens)
    
    def get_similar_word(self, comment: str):
        """Ищет похожие комметарии с comment"""
        pass

    def embedding(self) -> np.array:
        """Эмбеддинг для всех комментариев"""
        vectors = list()
        for comment in self.comments:
            vectors.append(self.get_vector(comment).tolist())
        self.vectors = np.array(vectors)
        return np.array(self.vectors)
            

    
    
    