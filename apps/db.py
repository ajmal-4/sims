from flask import Flask
from flask_pymongo import pymongo
from urllib.parse import quote_plus

password = "ajmal@1007"
encoded_password = quote_plus(password)

CONNECTION_STRING = f"mongodb+srv://ajmal:{encoded_password}@simscluster.cbs1x.mongodb.net/?retryWrites=true&w=majority&appName=simsCluster"

client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('simsdata')
clients_collection = db.get_collection('clients')
routes_collection = db.get_collection('routes')
products_collection = db.get_collection('products')