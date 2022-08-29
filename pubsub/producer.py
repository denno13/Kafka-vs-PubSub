import time
import random
import string

# Solace Python API modules from the solace package
from solace.messaging.messaging_service import MessagingService


# Imports for error handling
from solace.messaging.publisher.direct_message_publisher import PublishFailureListener
from solace.messaging.messaging_service import ReconnectionListener, ReconnectionAttemptListener, ServiceInterruptionListener 


# Import for topic subscribtion
from solace.messaging.resources.topic import Topic 


# Define broker properties as dict --> Settings for the PubSub+ Broker
# Basic settings for connectivity 
broker_prop = {
    "solace.messaging.transport.host": "localhost",
    "solace.messaging.service.vpn-name": "default",
    "solace.messaging.authentication.scheme.basic.username": "default",
    "solace.messaging.authentication.scheme.basic.password": "default"
}


# Initialize a messaging service 
# The builder is taking the properties from the broker_prop dict
messaging_service = MessagingService.builder().from_properties(broker_prop).build()


# Connecting to the messaging service
messaging_service.connect()


# Error handling for the messaging service (optional)
class ServiceEventHandler(ReconnectionListener, ReconnectionAttemptListener, ServiceInterruptionListener):
    def on_reconnected(self, event: "ServiceEvent"):
        print("\non_reconnected")
        print(f"Error cause: {event.get_cause() }")
        print(f"Message: {event.get_message()}")

    def on_reconnecting(self, event: "ServiceEvent"):
        print("\non_reconnecting")
        print(f"Error cause: {event.get_cause()}")
        print(f"Message: {event.get_message()}")

    def on_service_interrupted(self, event: "ServiceEvent"):
        print("\non_service_interrupted")
        print(f"Error cause: {event.get_cause() }")
        print(f"Message: {event.get_message()}")

# Error handling for publishing (optional)
class PublishErrorHandling(PublishFailureListener):
    def on_failed_publish(self, event: 'FailedPublishEvent'):
        print("on_failed_publish")


# Use class to initialize a service_handler for error handling
service_handler = ServiceEventHandler()
messaging_service.add_reconnection_listener(service_handler)
messaging_service.add_reconnection_attempt_listener(service_handler)
messaging_service.add_service_interruption_listener(service_handler)


# Create a publisher for messages
direct_publisher = messaging_service.create_direct_message_publisher_builder().build()
direct_publisher.set_publish_failure_listener(PublishErrorHandling())
direct_publisher.start()
print("Publisher running")


# Create a outbound message / data generator
message_body = ''.join(random.choice(string.ascii_letters)for _ in range(32))
outbound_message_builder = messaging_service.message_builder()\
    .with_property("Test", "PA2")\
    .with_property("Projektarbeit", "PubSub+")


# Testing
count = 1
print("Sending messages")
try:
    while True:
        while count <= 5:
            # Send messages to a one or more topics
            topic = Topic.of("beispiel/hallo/" + f"live/{count}")
            outbound_message = outbound_message_builder\
                .with_application_message_id(f"New {count}")\
                .build(message_body)
            direct_publisher.publish(destination=topic, message=outbound_message)
            print(f"Published message on {topic}")
            count += 1
            time.sleep(1)
        print("\n")
        count = 1
except KeyboardInterrupt:
    print("terminated")
    direct_publisher.terminate()
    messaging_service.disconnect()