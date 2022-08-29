import time 


# Solace Python API modules from the solace package
from solace.messaging.messaging_service import MessagingService


# Imports for error handling
from solace.messaging.messaging_service import ReconnectionListener, ReconnectionAttemptListener, ServiceInterruptionListener


# Import for topic subscribtion
from solace.messaging.resources.topic_subscription import TopicSubscription


# Import for message handling
from solace.messaging.receiver.message_receiver import MessageHandler


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
class ServiceEventHandler(ReconnectionAttemptListener, ReconnectionListener, ServiceInterruptionListener):
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

# Use class to initialize a service_handler for error handling
service_handler = ServiceEventHandler()
messaging_service.add_reconnection_listener(service_handler)
messaging_service.add_reconnection_attempt_listener(service_handler)
messaging_service.add_service_interruption_listener(service_handler)


# Create a reveicer for messages
# Define list of topics for subscribtion 
topics = ["beispiel/hallo/live/>", "beispiel/hallo/dennis/>"]
topic_sub = []  # TopicSubscribtion object for PubSub+

for topic in topics:
    topic_sub.append(TopicSubscription.of(topic))

direct_reveicer = messaging_service.create_direct_message_receiver_builder().with_subscriptions(topic_sub).build()
direct_reveicer.start()
print("Subscriber running")


# MessageHandler
# Define what the consumer will display when consuming messages
class MessageHandlerImpl(MessageHandler):
    def on_message(self, message: "InboundMessage"):
        #message_dump = str(message)
        #payload = message.get_payload_as_string()
        print(f"Message: {message}")
        #print(f"Payload: {payload}")


# Testing 
try:
    print(f"subscribing to:{topics}")
    direct_reveicer.receive_async(MessageHandlerImpl())

    try: 
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Disconnect Messaging Service")

finally:
    direct_reveicer.terminate()
    messaging_service.disconnect()