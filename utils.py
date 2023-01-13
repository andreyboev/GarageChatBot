from aiogram.types import FSInputFile

from chart_controller import generate_bar_chart
from db_controller import get_users_msg_count


def get_chart_activity_stat(chat_id):
    users_stat = get_users_msg_count(chat_id)
    names = []
    counts = []
    for name, count in users_stat:
        names.append(name)
        counts.append(count)
    generate_bar_chart(names, counts)
    fig = FSInputFile('fig.png')
    return fig