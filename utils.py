from aiogram.types import FSInputFile

from controllers.chart_controller import generate_bar_chart
from controllers.db_controller import get_users_msg_count


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


def get_right_bracket_word(count):
    if 10 < count % 100 < 15:
        return 'ногтей'
    elif count % 10 == 1:
        return 'ноготь'
    elif 1 < count % 10 < 5:
        return 'ногтя'
    else:
        return 'ногтей'
