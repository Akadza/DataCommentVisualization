import pandas as pd
import plotly.graph_objects as go
from collections import Counter

def plotCountComments(comments: list[str], title: str, save: bool = False):
    """
    График зависимости количества комментариев от количества символов в комментарии
    """
    comments_lenght = [len(comments) for comments in comments]
    comments_counts = Counter(comments_lenght)
    comments_counts = dict(sorted(comments_counts.items(), key=lambda item: item[0], reverse=False))

    df = pd.DataFrame(list(comments_counts.items()), columns=['comment_length', 'comment_count'])
    fig = go.Figure(data=go.Scatter(x=df['comment_length'], y=df['comment_count'], mode='lines'))
    fig.update_layout(title='Comment Count Depending on Comment Length',
                      xaxis_title='Comment Length',
                      yaxis_title='Comment Count')
    if (save):
        fig.write_image(f"GraphsPlotting/Graphs/{title}", width = 1980, height = 1080)

    fig.show()