from ensurepip import bootstrap
import time
import json
import random
from datetime import datetime
from data_generator import generate_message
from kafka import KafkaProducer


# Message serialized as JSON
def serializer(message):
    return json.dumps(message).encode('utf-8')


# Kafka Producer
producer = KafkaProducer(
    # Define where Kafka is localized
    bootstrap_servers='localhost:9092',
    value_serializer=serializer
)


try:
    while True:
        # Generate a message
        dummy_message = generate_message()
        # Send message to the 'message' topic
        print(
            f'Producing message - time: \
                {datetime.now()} ... Message = {str(dummy_message)}')
        producer.send('message', dummy_message)
        time.sleep(2)
except KeyboardInterrupt:
    print("terminated")
