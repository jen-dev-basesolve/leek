# flask/hello.py

from flask import Flask, jsonify
from celery import Celery
import os

app = Flask(__name__)
app.config["CELERY_BROKER_URL"] = os.environ['BROKER_URL'] 

celery = Celery(app.name, broker=os.environ['BROKER_URL'])
celery.conf.update(app.config)

@celery.task
def hello_world():
    return "<p>Hello, World!</p>"

@celery.task()
def add(x, y):
        return x + y

# @app.route('/')
# def add_task():
#   for i in range(10000):
#       add.delay(i, i)
#   return jsonify({'status': 'ok'})


# @app.route('/')
# def print_hello():
#     return '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>chichahic>>>>>>>>>>>>>>>>>>'