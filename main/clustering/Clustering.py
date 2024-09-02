import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN, KMeans
import plotly.express as px

class Clustering:
    def __init__(self, vectors: np.array = None, 
                 points: np.array = np.empty((0, 2)), 
                 comments: list[str] = None
                 ) -> None:
        """
        :param points: массив точек для двумерного пространства
        :      points: np.array[np.array[double]]
        """
        self.points = points # двумерный вектор
        self.vectors = vectors # многомерный вектор
        self.comments = comments # комментарии для вектора

    def generate_random_points(self, minV = -200, maxV = 200, n: int = 100) -> np.array:
        """
        Функция генерирования точек для теста кластеризации
        :param n: количество точек
        """
        self.points = np.random.randint(minV, maxV + 1, size=(n, 2))

    def cluster_DBscan(self, eps: int = 1, min_samples = 5):
        """
        Функция кластеризации точек DBscan
        :param eps: максимальное расстояние между точками в кластере
        :param min_samples: минимальное количество точек в кластере
        """
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        labels = dbscan.fit_predict(self.vectors)
        return labels
    
    def cluster_kMeans(self, n_clusters = 5):
        """
        Функция кластеризации точек KMeans
        :param n_clusters: количество кластеров
        """
        kmeans = KMeans(n_clusters = n_clusters)
        kmeans.fit(self.vectors)
        labels = kmeans.labels_ # кластеры
        center = kmeans.cluster_centers_ # центер кластера
        return labels, center

    def get_axes(self):
        """
        Возращает список точек для двумерного пространства self.points
        """
        if len(self.points[0]) != 2:
            print("self.points должен представлять двумерное пространство")
            return 0, 0
        x = self.points[:,0]
        y = self.points[:,1]
        return x, y
    
    def plot_clusters(self, eps: int = 10, n_clusters: int = 5, type: str = "dbscan", save: bool = True):
        """
        Построение двумерного графика точек с отображением кластеров по цветам
        :param eps: максимальное расстояние между точками в кластере (dbscan)
        :param n_cluster: количество кластеров (kmeans)
        :param type: тип алгоритма кластеризации (dbscan, kmeans)
        :param save: флаг сохранения графика
        """
        x, y = self.get_axes() # разделяем на координаты
        centers = None

        if (type == "dbscan"):
            labels = self.cluster_DBscan(eps=eps)
        elif (type == "kmeans"):
            labels, centers = self.cluster_kMeans(n_clusters=n_clusters)
        else:
            raise ValueError(f"Неверный алгоритм '{type}'.")
        
        x = [label**5 * xi if label != 0 else xi * 5 for label, xi in zip(labels, x) ]
        y = [label**5 * yi if label != 0 else yi * 5 for label, yi in zip(labels, y) ]
        #print(len(x), len(y), len(labels))
        data = pd.DataFrame({
            'x': x,
            'y': y,
            'label': labels,
            'text': self.comments
        })

        fig = px.scatter(data, x='x', y='y', color='label', hover_data={'text': True})
        fig.update_layout(title='Algorithm of {}'.format(type))
        fig.show()
        if (save):
            fig.write_image("plots/data-test-{}.png".format(type), width = 2550, height = 1440)
        if centers is not None and np.any(centers):
            return labels, centers
        else:
            return labels, None
    
    def transformation_to_points(self):
        for vector in self.vectors:
            vecXY = [vector[0], vector[1]]
            self.points = np.vstack([self.points, vecXY])
