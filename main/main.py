from PostgreConnect import PostgreConnect
from clustering import Clustering as cl
from GraphsPlotting import countComments as cgraph
import numpy as np
import time
from Embedding import Embedding
from Embeddingv2 import Embeddingv2
from vecToFile import saveVecToBin, loadVecFromBin 
from writeClusters import writeClusters
from readIni import ReadConfig 


def connect_to_db(dbName: str, table_name: str, link_list: list[str] = None):
    # подключение к DB
    if len(link_list) == 0: return None
    db = PostgreConnect(host="localhost",
                        database=dbName,
                        user="postgres",
                        password="WQkbwtwXX1")
    db.connect()
    db.create_table(table_name)

    start_time = time.time()
    i = 1
    # загрузка комментариев в бд-шку
    for link in link_list:
        try:
            list_c = db.load_Ytcomment(link) # иногда парсинг происходит с ошибкой
        except Exception as e:
            continue
        for comment in list_c:
            db.insert_comment(comment[0], comment[1])
        print("Progress: {}%".format(i / len(link_list) * 100))
        i += 1

    end_time = time.time()
    print("Добавление произошло за {} сек.".format(end_time - start_time))

    db.close()
    return 0


# кластеризация для dbscan и kmeans
def clustering(vectors: np.array, comments: list[str], eps: float, n_clusters: int):
    dbs = cl.Clustering(vectors=vectors, comments=comments)
    dbs.transformation_to_points()
    labels = dbs.plot_clusters(type="dbscan", eps=eps, save=True)
    writeClusters("dbscan", comments, labels[0].tolist())
    labels, centers = dbs.plot_clusters(type="kmeans", n_clusters=n_clusters, save=True)
    writeClusters("kMeans", comments, labels)
    print("процесс завершен")
    return 0

# график для n комменариев. соотношение количества к длине
def plotting_count_comments(comments: list[str], title: str, save=False):
    cgraph.plotCountComments(comments, title=title, save=save)
    

# эмбендинг для набора комментариев
def get_embedding(comments: list[str], vSize: int = 3):
    emb = Embedding(comments=comments, vSize=vSize)
    emb.embedding()

    return emb.vectors


def get_embeddingv2(comments: list[str], vec2: bool=True):
    """
    :param comments: список комментариев
    :param vec2: если True, то вернет точки, иначе - многомерные вектора
    """
    emb = Embeddingv2(comments=comments)
    emb.get_vectors()
    emb.get_points()
    if vec2:
        return emb.points
    else:
        return emb.vectors

# получение комментариев
def getDB_comments(dbname:str, tableName: str, count_comments: int) -> list[str]:
    db = PostgreConnect(host="localhost",
                        database=dbname,
                        user="postgres",
                        password="WQkbwtwXX1",
                        tableName=tableName)
    db.connect()
    comments = [comment[0] for comment in db.get_comments(count_comments, True)]
    db.close()
    return comments


def main():

    config = ReadConfig()
    db_settings = config.get_database_settings()
    
    # настройки с config.ini файла
    database_name: str = db_settings[0]
    table_name: str = db_settings[1]
    links: list[str] = config.get_links()

    outputConf1 = config.get_output1()
    count_comments: int = outputConf1[0]
    plot_comment_length_dependency: bool = outputConf1[1]
    plot_comment_length_dependency_save: bool = outputConf1[2]

    embeddingConf = config.get_embedding_config()
    count_comments: int = embeddingConf[0]
    have_vectors: bool = embeddingConf[1]
    eps: float = float(embeddingConf[2])
    n_clusters: int = int(embeddingConf[3])

    # начало процесса
    connect_to_db(database_name, table_name, links) # создание базы данных и загрузка комментов
    comments = getDB_comments(database_name, table_name, count_comments) # получение комментариев

    # построение графика
    if plot_comment_length_dependency == "yes":
        plotting_count_comments(comments, f"{table_name}.png", plot_comment_length_dependency_save)

    # эмбеддинг
    path = f"vecFiles/{table_name}.npy"
    if have_vectors == "yes":
        vectors = loadVecFromBin(file_path=path)
    else:
        vectors = get_embeddingv2(comments)
        saveVecToBin(file_path=path, vectors=vectors)
    
    # кластеризация
    clustering(vectors, comments, eps, n_clusters)
    
 
    return 0
    

if __name__ == "__main__":
    main()
