from kafka import KafkaProducer, KafkaConsumer
from datetime import datetime
import random
import time
import redis
import json

tweets = [
    "Just saw Elon Musk talking about SpaceX on TV.",
    "Apple is planning to release a new iPhone in California next month.",
    "Microsoft and Google are collaborating on AI research.",
    "Visited the Eiffel Tower in Paris last summer. Spectacular!",
    "Serena Williams wins another Grand Slam title!",
    "Met Dr. Smith at Harvard Medical School last week.",
    "Watching Batman in IMAX at AMC Theatres was amazing.",
    "Amazon just opened a new office in Seattle.",
    "I’m heading to New York for a conference.",
    "Tesla Model S is such a cool car!",
    "Got my new MacBook from Best Buy today.",
    "Barack Obama visited Kenya for a summit.",
    "Samsung’s Galaxy Watch is really sleek.",
    "Facebook is under scrutiny from the U.S. Senate.",
    "Lionel Messi joins Inter Miami!",
    "Delhi's street food is out of this world.",
    "Meta is investing heavily in the metaverse.",
    "Reading \"To Kill a Mockingbird\" by Harper Lee again.",
    "Attending a tech meetup at Googleplex.",
    "The World Cup final in Qatar was thrilling!",
    "Elon Musk and Jeff Bezos are always competing.",
    "Loved my visit to the Grand Canyon.",
    "Spotted a Jaguar in Ranthambore National Park.",
    "Oprah Winfrey spoke at Stanford today.",
    "Got some nice shoes from Nike’s new collection.",
    "Just landed in Tokyo for my Japan trip!",
    "Cristiano Ronaldo breaks another record.",
    "Got vaccinated at Mayo Clinic.",
    "Attending AWS re:Invent in Las Vegas!",
    "The Taj Mahal looks stunning at sunrise.",
    "Studying law at Yale University.",
    "Just got back from a safari in South Africa.",
    "My order from Zara arrived in just two days.",
    "The White House issued a new press release.",
    "Taylor Swift’s new album is trending.",
    "Ratan Tata supports young entrepreneurs.",
    "Google Maps helped us navigate the Alps.",
    "Saw a lion at the Bronx Zoo.",
    "The Eiffel Tower lit up at night is magical.",
    "Stanford is one of the top universities in the world.",
    "Bill Gates visited MIT last weekend.",
    "Got my iPad from the Apple Store.",
    "Kanye West launches his new fashion line.",
    "UberEats delivered from Domino’s Pizza in minutes!",
    "Got some cool merch from Marvel Studios.",
    "Just finished a documentary on Steve Jobs.",
    "Booked a hotel near Niagara Falls.",
    "Emma Watson advocates for gender equality.",
    "WeWork has a great workspace in Manhattan.",
    "My new drone from DJI is incredible!",
    "Had ramen in a cozy Tokyo café.",
    "Warren Buffett gives financial advice.",
    "Hiking in Yosemite National Park this weekend.",
    "AI generated art is displayed at the Louvre.",
    "Spoke to a recruiter from IBM.",
    "Ordered a Kindle from Amazon Prime.",
    "Attending a workshop at Columbia University.",
    "Jeff Bezos visits the Blue Origin site.",
    "Watching a cricket match at Lord’s.",
    "Delhi Metro is super convenient.",
    "Checking out the new Sony headphones.",
    "Joined an online class from Coursera.",
    "Got coffee from Starbucks in Berlin.",
    "Met an astronaut from NASA!",
    "Attending a wedding in San Francisco.",
    "Ice skating at Rockefeller Center!",
    "ChatGPT is trending on Twitter.",
    "My cousin studies at Oxford.",
    "Going skiing in Switzerland next week.",
    "Bought groceries from Walmart.",
    "Following the World Economic Forum updates.",
    "Watched a Broadway show at Times Square.",
    "Joined a webinar hosted by Khan Academy.",
    "Had dinner at a Michelin-starred restaurant in London.",
    "Following the trial updates from Washington D.C.",
    "Reading a new book by Dan Brown.",
    "H&M’s new winter collection is out!",
    "Took a selfie at the Hollywood Sign.",
    "Elon Musk tweets again!",
    "Booked tickets through Expedia.",
    "Cooking a recipe from Gordon Ramsay’s book.",
    "Meeting a friend at Central Park.",
    "Uber ride from JFK was smooth.",
    "Learning Python on Udemy.",
    "Got a new SIM from Verizon.",
    "Banking with JPMorgan Chase.",
    "Collecting Funko Pops from Marvel and DC.",
    "Flew Emirates to Dubai.",
    "Loved the beach in Malibu.",
    "Coding hackathon at Facebook HQ.",
    "Tracking my package from FedEx.",
    "Spoke to a professor from Princeton.",
    "Visited the CN Tower in Toronto.",
    "Baking with Nigella Lawson’s recipes.",
    "Trying out Peloton’s new bike.",
    "Following Tesla’s stock market movement.",
    "Snapped some photos at Yellowstone.",
    "Watching a live stream by NASA.",
    "Trying out the new Burger King veggie menu.",
    "Celebrating Diwali in Mumbai."
]


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
                "tweet_text": tweets[random.randint(0, 99)], 
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
