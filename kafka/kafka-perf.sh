# Producer Test
$ bin/kafka-topics.sh \
--create --zookeeper zookeeper:2181 \
--replication-factor 1 \
--partitions 1 \
--topic perf_test


$ bin/kafka-producer-perf-test.sh \
--topic perf-test \
--throughput -1 \
--num-records 30000000 \
--record-size 1024 \
--producer-props acks=all bootstrap.servers=localhost:9092 \

# Consumer Test
$ bin/kafka-consumer-perf-test.sh \
--topic perf-test \
--messages 3000000 \
--bootstrap-server localhost:9092 
