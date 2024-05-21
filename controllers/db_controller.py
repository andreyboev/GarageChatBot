import sqlite3

connection = sqlite3.connect('garage_data.db')


def has_user(chat_id, user_id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user WHERE user_id=? AND chat=?", (user_id, chat_id))
    result = cursor.fetchall()
    cursor.close()
    return len(result) > 0


def has_chat(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM chat WHERE id=?", (id,))
    result = cursor.fetchall()
    cursor.close()
    return len(result) > 0


def add_chat(chat_id, name):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO chat(id, name) VALUES (?, ?)", (chat_id, name))
    connection.commit()
    cursor.close()


def add_user(id, name, chat_id):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO user(user_id, name, message_count, chat) VALUES (?, ?, 0, ?)", (id, name, chat_id))
    connection.commit()
    cursor.close()


def update_user_name(id, name, chat_id):
    cursor = connection.cursor()
    cursor.execute("UPDATE user set name=? WHERE user_id=? AND chat=?", (name, id, chat_id))
    connection.commit()
    cursor.close()


def get_users(chat_id):
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM user WHERE chat=?", (chat_id,))
    result = [val[0] for val in cursor.fetchall()]
    cursor.close()
    return result


def get_user_info(id, chat_id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user WHERE user_id=? AND chat=?", (id, chat_id))
    result = cursor.fetchone()
    cursor.close()
    return result


def inc_user_msg_count(id, chat_id, count=1):
    cursor = connection.cursor()
    cursor.execute("SELECT message_count FROM user WHERE user_id=? AND chat=?", (id, chat_id))
    old_count = cursor.fetchone()[0]
    cursor.close()
    cursor = connection.cursor()
    old_count += count
    cursor.execute("UPDATE user set message_count=? WHERE user_id=? AND chat=?", (old_count, id, chat_id))
    connection.commit()
    cursor.close()


def get_users_msg_count(chat_id):
    cursor = connection.cursor()
    cursor.execute("SELECT name, message_count FROM user WHERE chat=?", (chat_id,))
    stat = cursor.fetchall()
    cursor.close()
    return stat


def inc_user_brackets_count(id, chat_id, count):
    cursor = connection.cursor()
    cursor.execute("SELECT brackets_count FROM user WHERE user_id=? AND chat=?", (id, chat_id))
    c = cursor.fetchone()[0]
    cursor.close()
    cursor = connection.cursor()
    c += count
    cursor.execute("UPDATE user set brackets_count=? WHERE user_id=? AND chat=?", (c, id, chat_id))
    connection.commit()
    cursor.close()
    return c


def get_next_obscene_phrase(chat_id):
    cursor = connection.cursor()
    cursor.execute("SELECT obscene_indexer FROM settings WHERE chat=?", (chat_id,))
    obscene_index = cursor.fetchone()
    if obscene_index is None:
        cursor.execute("INSERT INTO settings(chat, obscene_indexer) VALUES (?, 0)", (chat_id,))
        connection.commit()
        obscene_index = 0
    else:
        obscene_index = obscene_index[0]
        obscene_index += 1
        cursor.execute("UPDATE settings set obscene_indexer=? WHERE chat=?", (obscene_index, chat_id))
        connection.commit()

    cursor.execute("SELECT text FROM phrase WHERE type='Obscene'")
    phrases = cursor.fetchall()
    cursor.close()

    return phrases[obscene_index % len(phrases)][0]

