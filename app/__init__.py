from flask import Flask
import rocksdb

app = Flask(__name__)
db = rocksdb.DB("test.db", rocksdb.Options(create_if_missing=True))

from app import views