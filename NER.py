from kafka import KafkaConsumer
import boto3
import spacy
import json
from botocore.exceptions import ClientError

# Initialize spaCy NER model
nlp = spacy.load("en_core_web_sm")

# Initialize DynamoDB client
# dynamodb = boto3.resource('dynamodb', region_name='us-west-2')  # Change your region
dynamodb = boto3.resource(
    'dynamodb',
    region_name='us-east-1',  # Replace with your region
    aws_access_key_id='',
    aws_secret_access_key=''
)
table = dynamodb.Table('EntityCounts')  # Replace with your table name

# Kafka Consumer setup
# consumer = KafkaConsumer(
#     'your-topic-name',  # Replace with your Kafka topic
#     bootstrap_servers='your-broker:9092',  # Replace with your MSK broker
#     security_protocol='SASL_SSL',
#     sasl_mechanism='AWS_MSK_IAM',
#     sasl_plain_username='unused',
#     sasl_plain_password='unused',
#     group_id='ner-group',
#     auto_offset_reset='latest',
#     enable_auto_commit=True
# )

consumer = KafkaConsumer(
    'sample',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='ner-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Function to update count in DynamoDB
def update_entity_count(entity_text):
    try:
        # Try to update existing item
        table.update_item(
            Key={'Entity': entity_text},
            UpdateExpression="SET #cnt = if_not_exists(#cnt, :start) + :inc",
            ExpressionAttributeNames={"#cnt": "Count"},
            ExpressionAttributeValues={":inc": 1, ":start": 0}
        )
        print(f"entity -> {entity_text}")
    except ClientError as e:
        print(f"Error updating DynamoDB: {e.response['Error']['Message']}")

# Main consumer loop
print("Listening to Kafka topic...")
for message in consumer:
    try:
        # msg_text = message.value.decode('utf-8')
        # print(dynamodb.list_tables())
        message = message.value
        tweet_id = message["tweet_id"]
        tweet_text = message["tweet_text"]
        hashtags_selected = message["hashtags_selected"] 
        minute_index = message["minute_index"]
        # print("message", "tweet_id", "tweet_text", "hashtags_selected", "minute_index")
        # print(message, tweet_id, tweet_text, hashtags_selected, minute_index)

        # Perform NER
        doc = nlp(tweet_text)
        for ent in doc.ents:
            entity_text = ent.text.strip()
            update_entity_count(entity_text)
    except Exception as e:
        print(f"Processing error: {e}")
