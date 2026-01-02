from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)

MONGO_USER = os.environ.get("MONGO_USER")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")
MONGO_HOST = os.environ.get("MONGO_HOST", "mongodb")

mongo_uri = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:27017/flask_db?authSource=admin"

client = MongoClient(mongo_uri)
db = client.flask_db
collection = db.data

@app.route('/')
def index():
    return f"Welcome to the Rohit Flask app! The current time is: {datetime.now()}"

@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        collection.insert_one(request.json)
        return jsonify({"status": "Data inserted"}), 201
    return jsonify(list(collection.find({}, {"_id": 0}))), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
