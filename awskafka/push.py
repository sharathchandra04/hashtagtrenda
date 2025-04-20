from kafka import KafkaProducer

# Replace with your MSK Serverless Bootstrap Broker endpoint
BOOTSTRAP_SERVERS = ['boot-zvywiq58.c2.kafka-serverless.us-east-1.amazonaws.com:9098']

producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    security_protocol="SSL",  # Or "PLAINTEXT" if your MSK allows that (usually not recommended)
)

topic = 'your-topic-name'

for i in range(10):
    key = f'key-{i}'.encode('utf-8')
    value = f'Hello from Python! Message {i}'.encode('utf-8')
    future = producer.send(topic, key=key, value=value)
    result = future.get(timeout=10)
    print(f"✅ Sent: {result.topic} [Partition {result.partition}] Offset {result.offset}")

producer.flush()
producer.close()
