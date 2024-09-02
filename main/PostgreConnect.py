import psycopg2
from dialogWindows import error_db
from collectData import commentLoader as cload


class PostgreConnect:

    def __init__(self, host, database, user, password, tableName = None, port=5432):
        """
        :param host: адрес хоста
        :param database: название базы данных
        :param user: имя пользователя
        :param password: пароль подключения
        :param tableName: название таблицы, не указывайте конструтор по умолчанию 
                          для tableName, если таблицы не существует
        :param port: оставить по умолчанию, если вы не изменяли порт в настройках
        """
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.table_name = tableName
        self.connection = None
        self.cursor = None

    def create_table(self, tableName: str):
        """Создание новой таблицы"""
        self.table_name = tableName
        if self.connection is None:
            print("Database connection is not required")
            return 0
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS {} (
                    id SERIAL PRIMARY KEY,
                    author varchar(255) NOT NULL,
                    text varchar(6000) NOT NULL,
                    time timestamp,
                    tag varchar(255)
                )
            """.format(self.table_name))
            self.connection.commit()
        except Exception as e:
            error_db("Error creating table\nError:", e)
            return 0

    def connect(self):
        """Открывает сессию подключения к database"""
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port,
            )
            self.cursor = self.connection.cursor()
        except (Exception, psycopg2.Error) as error:
            error_db("failed to connect to the database, check the data is correct\nError:", error)
            return

    def insert_comment(self, author: str, text: str, time = None, tag: str = None):
        """Добавляет данные комментария в базу данных"""
        try:
            self.cursor.execute('''
                INSERT INTO {} (author, text, time, tag) VALUES (%s, %s, %s, %s)
            '''.format(self.table_name), (author, text, time, tag))
            self.connection.commit()
        except Exception as e:
            print(f"Error inserting comment: {e}")
            return 0

    def execute_query(self, query: str) -> list:
        """Выполняет запрос query текущей сессии"""
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except (Exception, psycopg2.Error) as error:
            error_db("Error while executing request\nError:", error)
            return []
        
    def get_comments(self, count: int = 1, onlyComments: bool = False) -> list:
        """Возвращает список комментариев из бд-шки
        :param count: количество комментариев
        :param onlyComments: если True, то вернет только комментарии поля text
        """
        try:
            if onlyComments:
                self.cursor.execute('''
                    SELECT text FROM {} LIMIT {}
                '''.format(self.table_name, count))
            else:
                self.cursor.execute('''
                    SELECT * FROM {} LIMIT {}
                '''.format(self.table_name, count))                
            return self.cursor.fetchall()
        except (Exception, psycopg2.Error) as error:
            error_db("Error while executing request\nError:", error)
            return []

    def load_Ytcomment(self, link: str):
        """Загружает комментарии с видео ютуба по ссылке"""
        list_comments = cload.commentLoadYt(link)
        return list_comments

    def delete_table(self, tableName):
        """Удаляет таблицу tableName"""
        try:
            self.cursor.execute("""
                DROP TABLE IF EXISTS {}
            """.format(tableName))
            self.connection.commit()
        except (Exception, psycopg2.Error) as error:
            error_db("error delet table\nError:", error)
            return 0

    def close(self):
        """Закрывает текущее подключение"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
