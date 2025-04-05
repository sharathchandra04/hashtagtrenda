from kafka import KafkaProducer, KafkaConsumer
from datetime import datetime
import random
import time
import redis
import json

hashtags = None
weights = None

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',  # Replace with your Kafka server
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
    
def kafka_push(d):
    data = d
    producer.send('sample', value=data)
    print("Message sent!")

def generate_users(user_count):
    """Generate a dictionary of user IDs with random tweet counts."""
    return {f'user_{i}': random.randint(1, 1000) for i in range(1, user_count + 1)}

def generate_user_list(user_count):
    """Generate a list of user IDs."""
    return [f'user_{i}' for i in range(1, user_count + 1)]

# = zip(*hashtag_weights.items())  # Unpack the dictionary into separate lists
def edithasprob(index, weight):
    weights[index-1] = weight

def generate_hashtags_with_weights(num_hashtags):
    """Generate a list of random hashtags based on custom weights."""
    # Use random.choices to pick hashtags according to their weights
    # hashtags, weights = zip(*hashtag_weights.items())  # Unpack the dictionary into separate lists
    return random.choices(hashtags, weights=weights, k=num_hashtags)

def generate_tweet(user_tweet_map, country_list):
    """Generate a random tweet with a unique tweet ID."""
    now = datetime.now()
    minute_index = now.hour * 60 + now.minute
    user_id = random.choice(list(user_tweet_map.keys()))
    country_id = random.choice(country_list)
    hashtagsi = generate_hashtags_with_weights(random.randint(1, 4))
    tweet_id = f"{user_id}_{user_tweet_map[user_id]}"
    user_tweet_map[user_id] += 1
    tweet_text = f"User {user_id} from country:{country_id} says: {' '.join(hashtagsi)}"
    return tweet_id, tweet_text, hashtagsi, minute_index

if __name__ == "__main__":
    user_tweet_map = generate_users(1000)  # Generate a dictionary of 1000 user IDs with tweet counts
    user_list = generate_user_list(1000)  # Generate a separate list of 1000 user IDs
    country_list = list(range(1, 251))  # Generate a list of 250 country IDs
    hashtag_list = [i for i in range(1, 5000)]  # Generate 10,000 unique hashtags
    hashtag_weights = {f"#Tag{i}": random.randint(1, 10) for i in hashtag_list}  # Example weights
    hashtag_weights['#Tag500'] = 5000
    hashtag_weights['#Tag501'] = 9000
    hashtag_weights['#Tag502'] = 10000
    hashtags, weights = zip(*hashtag_weights.items())  # Unpack the dictionary into separate lists
    weights=list(weights)
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',  # Replace with your Kafka server
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    try:
        while True:
            tweet_id, tweet_text, hashtags_selected, minute_index = generate_tweet(user_tweet_map, country_list)
            data = {
                "tweet_id": tweet_id, 
                "tweet_text": tweet_text, 
                "hashtags_selected": hashtags_selected, 
                "minute_index": minute_index
            }
            print(data)
            # print(hashtags[0:10])
            producer.send('sample', value=data)
            redis_key = 'hash_weights'
            # 1. Check if key exists
            if redis_client.exists(redis_key):
                print("key present")
                trends = redis_client.hgetall(redis_key)  # returns a dict: { hashtag: weight, ... }
                for i in trends:
                    j = int(i[1:])
                    weights[j-1] = int(trends[i])
                redis_client.delete(redis_key)
            time.sleep(1)
    finally:
        producer.flush()
        producer.close()
