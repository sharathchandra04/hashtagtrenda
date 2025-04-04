import time
import redis
from kafka.admin import KafkaAdminClient, NewTopic

# Redis Configuration
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'  # Update if needed
TOPIC_NAME = "sample"

# Step 1: Clear Redis Database 0
for key in redis_client.keys('*'):
    redis_client.delete(key)
print("All keys deleted from Redis database 0.")
# Step 2: Delete Kafka Topic 'sample'
admin_client = KafkaAdminClient(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)

try:
    admin_client.delete_topics([TOPIC_NAME])
    print(f"Kafka topic '{TOPIC_NAME}' deleted successfully.")
except Exception as e:
    print(f"Failed to delete topic '{TOPIC_NAME}': {e}")

time.sleep(5)
# Step 3: Recreate Kafka Topic 'sample'
try:
    topic = NewTopic(name=TOPIC_NAME, num_partitions=1, replication_factor=1)
    admin_client.create_topics([topic])
    print(f"Kafka topic '{TOPIC_NAME}' created successfully.")
except Exception as e:
    print(f"Failed to create topic '{TOPIC_NAME}': {e}")

# Close Kafka Admin Client
admin_client.close()

# bin/zookeeper-server-start.sh config/zookeeper.properties
# bin/kafka-server-start.sh config/server.properties
# kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic sample
# bin/kafka-topics.sh --create --replication-factor 1 --partitions 1 --bootstrap-server localhost:9092 --topic sample
# bin/kafka-topics.sh --list --bootstrap-server localhost:9092
