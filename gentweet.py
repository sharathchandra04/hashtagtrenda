import random
from datetime import datetime
import time
import redis
from kafka import KafkaConsumer
import json

#############################################################
#############################################################
#############################################################

def calculate_hashtag_trends(redis_client, pres_set, prev_set, minute_index):
    decay_factor = 0.9
    # Fetch both sorted sets at once
    pres_data = redis_client.zrange(pres_set, 0, -1, withscores=True)
    prev_data = redis_client.zrange(prev_set, 0, -1, withscores=True)
    # Convert to dictionary {hashtag: count}
    pres_dict = {tag: count for tag, count in pres_data}
    prev_dict = {tag: count for tag, count in prev_data}
    # Get all unique hashtags from both sets
    all_hashtags = set(pres_dict.keys()).union(prev_dict.keys())
    trend_scores = {}
    # Calculate scores for each hashtag
    for hashtag in all_hashtags:
        pres_count = pres_dict.get(hashtag, 0)  # Default to 0 if not present
        prev_count = prev_dict.get(hashtag, 0)  # Default to 0 if not present
        velocity = pres_count - prev_count
        score = (pres_count * 0.6) + (velocity * 0.4) * decay_factor
        trend_scores[hashtag] = score
    # Store the scores back in Redis
    if trend_scores:
        redis_client.zadd(f"trend_scores_{minute_index}", trend_scores)
    return trend_scores

'''
if velocity > 50:  # Arbitrary threshold, tweak based on data
    print(f"🚀 Viral Alert! {hashtag} is trending FAST!")
'''
#############################################################
#############################################################
#############################################################


# bin/zookeeper-server-start.sh config/zookeeper.properties
# bin/kafka-server-start.sh config/server.properties
# kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic sample
# bin/kafka-topics.sh --create --replication-factor 1 --partitions 1 --bootstrap-server localhost:9092 --topic sample
# bin/kafka-topics.sh --list --bootstrap-server localhost:9092
if __name__ == "__main__":
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
    current_minute = None
    counter = 0
    consumer = KafkaConsumer(
        'sample',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        group_id='my-group',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    for message in consumer:
        message = message.value
        print(message)
        tweet_id = message["tweet_id"]
        tweet_text = message["tweet_text"]
        hashtags_selected = message["hashtags_selected"] 
        minute_index = message["minute_index"]
        if current_minute != minute_index:
            counter = counter + 1
            print("Minute changed.")
            current_minute = minute_index
            if current_minute != None and counter >= 4:
                print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                print('minute changed and counter increased')
                print(current_minute-3, current_minute-2, current_minute-1)
                if current_minute >= 3:
                    timestamp_str_before = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                    redis_client.zunionstore(
                        f"trending_combined_{current_minute-1}", 
                        [f"trending_{current_minute-3}", f"trending_{current_minute-2}", f"trending_{current_minute-1}"],
                        aggregate='sum'
                    )
                    calculate_hashtag_trends(
                        redis_client, 
                        f"trending_combined_{current_minute-1}",
                        f"trending_combined_{current_minute-2}", 
                        current_minute-1
                    )
                    timestamp_str_after = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                    print("Timestamp diff --> ", timestamp_str_before, timestamp_str_after)
                print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        time.sleep(1)
        for hashtag in hashtags_selected:
            hs = f"{hashtag}{minute_index}"
            redis_client.zincrby(f"trending_{minute_index}", 1, hashtag)
