from flask import Flask, jsonify, send_from_directory
import os
from redis import Redis
from datetime import datetime
redis_client = Redis(host='localhost', port=6379, db=0, decode_responses=True)

app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')

# @app.route('/api/get-trends')
# def get_trends():
#     trends = [
#         {"hashtag": "#AI", "count": 1200},
#         {"hashtag": "#Python", "count": 950},
#         {"hashtag": "#Flask", "count": 500}
#     ]
#     return jsonify(trends)

@app.route('/api/get-trends')
def get_trends():
    now = datetime.now()
    minute_index = now.hour * 60 + now.minute
    # redis_key = f"trend_scores_{minute_index-1}"
    redis_key = f"trend_scores_1422"
    trends_raw = redis_client.zrevrange(redis_key, 0, -1, withscores=True)
    trends = [{"hashtag": hashtag, "count": int(score)} for hashtag, score in trends_raw]
    return jsonify(trends)

@app.route('/')
def serve(path=""):
    if path != "" and os.path.exists(app.static_folder):
        return send_from_directory(app.static_folder)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
