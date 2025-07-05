from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# Connect to local MongoDB or use MongoDB Atlas
client = MongoClient("mongodb://localhost:27017/")
db = client["webhook_db"]
collection = db["events"]

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Format the timestamp
    try:
        data["timestamp"] = datetime.strptime(data["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
    except:
        data["timestamp"] = datetime.utcnow()

    collection.insert_one(data)
    return jsonify({"message": "Data saved to MongoDB"}), 200

@app.route("/events", methods=["GET"])
def get_events():
    events = list(collection.find({}, {"_id": 0}))
    return jsonify(events)

if __name__ == "__main__":
    app.run(debug=True)
  
