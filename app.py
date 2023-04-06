# flask/hello.py

from flask import Flask, jsonify
from celery import Celery
from redis import Redis
#from kombu import Queue
import os

app = Flask(__name__)           # initiating a flask app
celery = Celery(app.name, 
                broker=os.environ.get('broker_url'),
                backend = os.environ.get('result_backend'),
                task_send_sent_event = True)        # after setting task_send_set_event = True in file as well as docker comose, why is it still not showing proper task status in leek

celery.conf.update({"CELERY_SEND_TASK_SENT_EVENT":True,
                    "CELERY_ROUTES":{"queue":"celery"},   # celery tasks will be routed to queue
                    "CELERY_DEFAULT_EXCHANGE":"tasks"
                    #"CELERY_QUEUES":(Queue("app", routing_key="app"))        - This gives error as Queue is not iterable      
                    })
redis = Redis(host='redis',port=6379)



@app.route('/')         # print the below message on a  webpage.
def hello():
    return '<h1> Hello 1st step </h1>'


@celery.task            # This will form a celery object,which will not be executed in the flask terminal, but in the celery terminal
def hello_cellery():
    message='<h1>>>>>>>>>>>>>>>>>> Hi From Celery <<<<<<<<<<<<<<<<<<<<</h1>'
    return message

@celery.task
def add(x,y):
    sum = x+y
    return sum


@app.route('/celery')         # prints the message recived from hello_cellery is printed on /celery page.
def aftercelery():
    num = add.delay(5,15).get()
    return f'{num}' 

if __name__=='__main__':
    app.run(host="0.0.0.0",debug=True)
