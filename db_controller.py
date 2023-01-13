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


def get_user_info(id, chat_id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user WHERE user_id=? AND chat=?", (id, chat_id))
    result = cursor.fetchone()
    cursor.close()
    return result


def inc_user_msg_count(id, chat_id):
    cursor = connection.cursor()
    cursor.execute("SELECT message_count FROM user WHERE user_id=? AND chat=?", (id, chat_id))
    count = cursor.fetchone()[0]
    cursor.close()
    cursor = connection.cursor()
    count += 1
    cursor.execute("UPDATE user set message_count=? WHERE user_id=? AND chat=?", (count, id, chat_id))
    connection.commit()
    cursor.close()


def get_users_msg_count(chat_id):
    cursor = connection.cursor()
    cursor.execute("SELECT name, message_count FROM user WHERE chat=?", (chat_id,))
    stat = cursor.fetchall()
    cursor.close()
    return stat