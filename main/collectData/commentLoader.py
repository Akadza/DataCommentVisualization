from youtube_comment_downloader import *

def commentLoadYt(link: str) -> list[tuple]:
    """
    возращает комментарии к видео
    :param link: Ютуб ссылка на видео
    :param params: Параметры запроса, author, time и прочие
    :return: список данных комментариев
    """
    downloader = YoutubeCommentDownloader()
    comments = downloader.get_comments_from_url(link, sort_by=SORT_BY_POPULAR)
    comment_data = [(c['author'], c['text']) for c in comments]
    return comment_data
    