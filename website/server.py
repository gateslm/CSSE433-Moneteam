# Python code to be the main server file

from flask import Flask, render_template

import connections
from pymongo import MongoClient
import pymonetdb
import redis
import json
from bson.objectid import objectid
import ast


mongoClient = MongoClient() # TODO: Add the connection info
monetClient = connections.monetConn() # TODO: Add the connection info
redisClient = redis.Redis() # TODO: Add the connection info
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
