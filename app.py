from flask import Flask
from flask import request
from flask import jsonify
from flask import Response
from flask import redirect
from gevent.pywsgi import WSGIServer
from pymongo import MongoClient
from pprint import pprint
from time import time
import random
import json
# from connection import Connections
import awsconfig


app = Flask(__name__)

secret = {}
try:
    secret = json.loads(open('credentials.json').read())
except FileNotFoundError as err:
    print('FileNotFoundError')

    # Server config for local
    secret['host'] = 'localhost'
    secret['port'] = '27017'
    secret['db'] = 'embody-stager'

def dbInit():
    try:
        dbnames = connection.list_database_names()
        if secret['db'] not in dbnames:
            db_api = connection[secret['db']].releaseinfo
            db_api.insert_one({
                "Author":"Prateek Rokadiya",
                "buildtime": str(time()),
                "methods": "get, post, put, delete",
                "version": "v1"
            })
            print ("Database Initialize completed!")
        else:
            print ("Database already Initialized!")
    except:
        print ("Database creation Failed!!")

if __name__ == '__main__':
    s3_client = awsconfig.connect_s3()
    dbInit()

    # Debug/Development
    # app.run(host='127.0.0.1', port=5001)

    # Production
    listener:tuple = ('', 5001)
    print("Running on http://{}:{}/".format((listener[0] or "127.0.0.1"), listener[1]))
    http_server = WSGIServer(listener, app)
    http_server.serve_forever()
