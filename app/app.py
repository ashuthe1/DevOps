from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://mongo:27017/")
db = client['flaskdb']
collection = db['users']

# Create
@app.route('/create', methods=['POST'])
def create_user():
    data = request.json
    user_id = collection.insert_one(data).inserted_id
    return jsonify(str(user_id)), 201

# Read
@app.route('/users', methods=['GET'])
def get_users():
    users = list(collection.find())
    for user in users:
        user['_id'] = str(user['_id'])
    return jsonify(users), 200

# Update
@app.route('/update/<id>', methods=['PUT'])
def update_user(id):
    data = request.json
    collection.update_one({'_id': ObjectId(id)}, {'$set': data})
    return jsonify({"message": "User updated!"}), 200

# Delete
@app.route('/delete/<id>', methods=['DELETE'])
def delete_user(id):
    collection.delete_one({'_id': ObjectId(id)})
    return jsonify({"message": "User deleted!"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)