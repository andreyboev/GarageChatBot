import pymysql

connection = pymysql.connect(host='95.163.233.154',
                             user='andreyboev',
                             password='aQ123!+',
                             database='garage_data',
                             port=3310)


def has_user(chat_id, user_id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user WHERE user_id=%s AND chat=%s", (user_id, chat_id))
    result = cursor.fetchall()
    cursor.close()
    return len(result) > 0


def has_chat(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM chat WHERE id=%s", (id,))
    result = cursor.fetchall()
    cursor.close()
    return len(result) > 0


def add_chat(chat_id, name):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO chat(id, name) VALUES (%s, %s)", (chat_id, name))
    connection.commit()
    cursor.close()


def add_user(id, name, chat_id):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO user(user_id, name, message_count, chat) VALUES (%s, %s, 0, %s)", (id, name, chat_id))
    connection.commit()
    cursor.close()


def update_user_name(id, name, chat_id):
    cursor = connection.cursor()
    cursor.execute("UPDATE user set name=%s WHERE user_id=%s AND chat=%s", (name, id, chat_id))
    connection.commit()
    cursor.close()


def get_users(chat_id):
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM user WHERE chat=%s", (chat_id,))
    result = [val[0] for val in cursor.fetchall()]
    cursor.close()
    return result


def get_user_info(id, chat_id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user WHERE user_id=%s AND chat=%s", (id, chat_id))
    result = cursor.fetchone()
    cursor.close()
    return result


def inc_user_msg_count(id, chat_id, count=1):
    cursor = connection.cursor()
    cursor.execute("SELECT message_count FROM user WHERE user_id=%s AND chat=%s", (id, chat_id))
    old_count = cursor.fetchone()[0]
    cursor.close()
    cursor = connection.cursor()
    old_count += count
    cursor.execute("UPDATE user set message_count=%s WHERE user_id=%s AND chat=%s", (old_count, id, chat_id))
    connection.commit()
    cursor.close()


def get_users_msg_count(chat_id):
    cursor = connection.cursor()
    cursor.execute("SELECT name, message_count FROM user WHERE chat=%s", (chat_id,))
    stat = cursor.fetchall()
    cursor.close()
    return stat

def get_users_brackets_count(id, chat_id):
    cursor = connection.cursor()
    cursor.execute("SELECT total_brackets_count, brackets_count FROM user WHERE user_id=%s AND chat=%s", (id, chat_id))
    stat = cursor.fetchone()
    cursor.close()
    return stat

def inc_user_brackets_count(id, chat_id, count):
    stat = get_users_brackets_count(id, chat_id)
    cursor = connection.cursor()
    c = count + stat[1]
    total_count = stat[0] + count
    cursor.execute("UPDATE user set total_brackets_count=%s, brackets_count=%s WHERE user_id=%s AND chat=%s", (total_count, c, id, chat_id))
    connection.commit()
    cursor.close()


def get_next_obscene_phrase(chat_id):
    cursor = connection.cursor()
    cursor.execute("SELECT obscene_indexer FROM settings WHERE chat=%s", (chat_id,))
    obscene_index = cursor.fetchone()
    if obscene_index is None:
        cursor.execute("INSERT INTO settings(chat, obscene_indexer) VALUES (%s, 0)", (chat_id,))
        connection.commit()
        obscene_index = 0
    else:
        obscene_index = obscene_index[0]
        obscene_index += 1
        cursor.execute("UPDATE settings set obscene_indexer=%s WHERE chat=%s", (obscene_index, chat_id))
        connection.commit()

    cursor.execute("SELECT text FROM phrase WHERE type='Obscene'")
    phrases = cursor.fetchall()
    cursor.close()

    return phrases[obscene_index % len(phrases)][0]

