
write following content to it.

1. install redis
2. install redis insight to visualise the redis
3. download kafka
4. run zookeeper
5. run kafka
6. create a kafka topic called sample
7. open two different terminals and run two python files
python readtweet.py (terminal 1)
python generate_tweets.py (terminal 2)

incase if you want to clear the resources (flush redis database & kafka topic)
python resource_reset.py

# bin/zookeeper-server-start.sh config/zookeeper.properties
# bin/kafka-server-start.sh config/server.properties
# kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic sample
# bin/kafka-topics.sh --create --replication-factor 1 --partitions 1 --bootstrap-server localhost:9092 --topic sample
# bin/kafka-topics.sh --list --bootstrap-server localhost:9092
