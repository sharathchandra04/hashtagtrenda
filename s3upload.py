import json
import csv
import uuid
import boto3
from kafka import KafkaConsumer
import spacy

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Kafka Consumer
consumer = KafkaConsumer(
    'sample',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='s3-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# AWS S3 Setup
s3 = boto3.client(
    's3',
    region_name='us-east-1',
    aws_access_key_id='',
    aws_secret_access_key=''
)

bucket_name = 'arsctweets'

# Buffer to hold messages
message_buffer = []
BATCH_SIZE = 10

def flush_buffer_to_s3():
    global message_buffer

    if not message_buffer:
        return

    filename = f"tweets_batch_{uuid.uuid4().hex[:8]}.csv"

    # Write to CSV
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["tweet_id", "tweet_text", "hashtags_selected", "minute_index"])
        for msg in message_buffer:
            writer.writerow([
                msg["tweet_id"],
                msg["tweet_text"],
                ','.join(msg["hashtags_selected"]),
                msg["minute_index"]
            ])

    # Upload to S3
    try:
        s3.upload_file(filename, bucket_name, filename)
        print(f"Uploaded {filename} to S3 bucket '{bucket_name}'")
    except Exception as e:
        print(f"Failed to upload to S3: {e}")

    # Clear buffer
    message_buffer = []

# Main Kafka consumer loop
print("Listening to Kafka topic...")
for message in consumer:
    try:
        msg = message.value

        # Extract NER entities
        doc = nlp(msg["tweet_text"])
        entities = [ent.text.strip() for ent in doc.ents]

        # Enrich and buffer message
        enriched = {
            "tweet_id": msg["tweet_id"],
            "tweet_text": msg["tweet_text"],
            "hashtags_selected": msg["hashtags_selected"],
            "minute_index": msg["minute_index"],
            "entities": entities
        }

        message_buffer.append(enriched)

        # Flush every 1000 messages
        if len(message_buffer) >= BATCH_SIZE:
            flush_buffer_to_s3()

    except Exception as e:
        print(f"Processing error: {e}")
