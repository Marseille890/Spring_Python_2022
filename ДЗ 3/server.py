# save this as app.py
import random
import time
from datetime import datetime

import flask
from flask import Flask, abort

app = Flask(__name__)
db = []
for i in range(3):
    db.append({
        'name': 'Anton',
        'time': 12343,
        'text': 'text01923097'
    })

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/send", methods= ['POST'])
def send_message():
    '''
    функция для отправки нового сообщения пользователем
    :return:
    '''
    data = flask.request.json
    if not isinstance(data, dict):
        return abort(400)

    if 'name' not in data or \
        'text' not in data:
        return abort(400)

    if not isinstance(data['name'], str) or \
        not isinstance(data['text'], str) or \
        len(data['name']) == 0 or \
        len(data['text']) == 0:
        return abort(400)

    text = data['text']
    name = data['name']

    if text[0] == '***':
        name = 'Анонимус'

    message = {
        'text': text,
        'name': name,
        'time': time.time()
    }

    if text == '/help':
        message['text'] = 'Начните сообщение со звездочек (***), чтобы отправить его анонимно. ' \
                          'Введите /clear, если хотите очистить историю сообщений. ' \
                          'Введите /clear=name, если хотите удалить последнее сообщение пользователя name. ' \
                          'Введите /time, если хотите узнать, сколько прошло секунд с 1 января 1970 года'
        message['name'] = 'server'
        db.append(message)
    elif text == '/clear':
        db.clear()
        message['text'] = 'История очищена'
        message['name'] = 'server'
        db.append(message)
    elif text[:7] == '/clear=':
        n = text[7:]
        for i in range((len(db) - 1), -1, -1):
            if db[i]['name'] == n:
                db.pop(i)
                break
        message['text'] = f'{name} удалил(а) последнее сообщения пользователя {n}'
        message['name'] = 'server'
        db.append(message)
    elif text == '/time':
        message['text'] = time.time()
        message['name'] = 'server'
        db.append(message)
    else:
        db.append(message)

    return {'ok': True}

@app.route("/messages")
def get_messages():
    try:
        after = float(flask.request.args['after'])
    except:
        abort(400)
    db_after = []
    for message in db:
        if message['time'] > after:
            db_after.append(message)
    return {'messages': db_after}

@app.route("/status")
def print_status():
    names = set()
    for i in db:
        names.add(i['name'])

    return f'Количество сообщений: {len(db)}, количество участников: {len(names)} ({", ".join(names)})'



app.run()