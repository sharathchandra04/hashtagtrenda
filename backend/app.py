from flask import Flask, request, jsonify, send_from_directory
import os
from redis import Redis
from datetime import datetime
from flask_cors import CORS
import redis

# from confluent_kafka import Consumer, KafkaException
from collections import defaultdict

redis_client = Redis(host='localhost', port=6379, db=0, decode_responses=True)

app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')
CORS(app)  # This enables CORS for all routes and all origins

# kafka_config = {
#     'bootstrap.servers': 'localhost:9092',
#     'group.id': 'hashtag-api-consumer',
#     'auto.offset.reset': 'earliest'
# }

# topic = 'hashtags'

# # Create Kafka consumer
# consumer = Consumer(kafka_config)
# consumer.subscribe([topic])


from kafka import KafkaConsumer

# Initialize Kafka consumer
consumer = KafkaConsumer(
    'hashtags',  # Topic name
    bootstrap_servers='localhost:9092',  # Change if necessary
    auto_offset_reset='earliest',  # Read from the beginning of the topic
    enable_auto_commit=True,
    key_deserializer=lambda k: k.decode() if k else None,
    value_deserializer=lambda v: v.decode() if v else None
)

# Read and print messages from Kafka
@app.route('/api/hashtags', methods=['GET'])
def get_hashtag_counts():
    hashtag_counts = defaultdict(int)
    messages_polled = 0
    threshold = 0
    data = request.get_json()
    for message in consumer:
        threshold = threshold + 1
        # print(f"Key={message.key}, Value='{message.value}'")
        hashtag = message.value
        if hashtag and hashtag == data.hashtag:
            hashtag_counts[hashtag] += 1
            messages_polled += 1
        if threshold>15:
            break

    return jsonify(dict(hashtag_counts))

@app.route('/api/get-trends')
def get_trends():
    print("------")
    now = datetime.now()
    minute_index = now.hour * 60 + now.minute
    redis_key = f"trend_scores_{minute_index-1}"
    print("curr redis key ---->   ", redis_key)
    if not redis_client.exists(redis_key):
        return jsonify([]), 404    
    trends_raw = redis_client.zrevrange(redis_key, 0, 9, withscores=True)
    # print('trends_raw --> ', trends_raw)
    trends = [{"hashtag": hashtag, "count": int(score)} for hashtag, score in trends_raw]
    return jsonify(trends)

@app.route('/api/update-trends', methods=['POST'])
def update_trends():
    try:
        data = request.get_json()
        print("Received trends data:", data)
        if not isinstance(data, dict):
            return jsonify({"error": "Invalid data format. Expected a key-value map."}), 400
        # Set Redis hash with key 'hash_weight'
        redis_key = 'hash_weights'
        redis_client.hset(redis_key, mapping=data)
        return jsonify({"message": "Trends updated in Redis."}), 200
    except Exception as e:
        print("Error in update_trends:", str(e))
        return jsonify({"error": "Server error"}), 500

@app.route('/')
def serve(path=""):
    if path != "" and os.path.exists(app.static_folder):
        return send_from_directory(app.static_folder)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)