from ensurepip import bootstrap
import json
from kafka import KafkaConsumer

print("consuming messages")
try:
    while True:
    # Kafka Consumer
        consumer = KafkaConsumer(
            # Define topic which will be consumed
            'message',
            bootstrap_servers='localhost:9092',
            auto_offset_reset='earliest'
        )
        for message in consumer:
            print(json.loads(message.value))
except KeyboardInterrupt:
    print("terminated")
    
