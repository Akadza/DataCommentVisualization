from bs4 import BeautifulSoup
from PostgreConnect import PostgreConnect

table_name = 'tg_comments'
dbName = 'DataVisualizationComments'

def main():
    db = PostgreConnect(host="localhost",
                        database=dbName,
                        user="postgres",
                        password="WQkbwtwXX1")
    db.connect()
    db.create_table(table_name)

    for i in range(2, 71):
        with open(f'chatHistory/messages{i}.html', 'r', encoding='utf-8') as file:
            content = file.read()

        soup = BeautifulSoup(content, 'lxml')
        comments = soup.find_all('div', class_='text')
        authors = soup.find_all('div', class_='from_name')

        for comment, author in zip(comments, authors):
            #print(f' {author.text.strip()}: {comment.text.strip()}')
            db.insert_comment("NULL", comment.text.strip())


    return 0


if __name__ == '__main__':
    main()