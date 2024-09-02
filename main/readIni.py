import configparser

class ReadConfig:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

    def get_database_settings(self) -> tuple:
        """Получаем настройки базы данных"""
        db_name = self.config.get('database', 'database_name')
        table_name = self.config.get('database', 'table_name')
        return db_name, table_name
    
    def get_links(self) -> list[str]:
        """Получаем ссылки"""
        try:
            links = self.config.get('links', 'urls').split(',')
        except Exception as e:
            return []
        return links
    
    def get_output1(self) -> tuple:
        """Получаем настройки вывода 1"""
        count_comments = self.config.get('output1', 'count_comments')
        plot_comment_length_dependency = self.config.get('output1', 'plot_comment_length_dependency')
        plot_comment_length_dependency_save = self.config.get('output1', 'plot_comment_length_dependency_save')
        title_graph = self.config.get('output1', 'title_graph')
        return count_comments, plot_comment_length_dependency, plot_comment_length_dependency_save, title_graph
    
    def get_embedding_config(self) -> tuple:
        """настройки эмбеддинга"""
        count_comments = self.config.get('embedding', 'count_comments')
        have_vectors = self.config.get('embedding', 'have_vectors')
        eps = self.config.get('embedding', 'eps')
        n_clusters = self.config.get('embedding', 'n_clusters')
        return count_comments, have_vectors, eps, n_clusters
        