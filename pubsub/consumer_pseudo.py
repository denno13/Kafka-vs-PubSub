# Basic settings for connectivity 
broker_prop = {
    "solace.messaging.transport.host": "localhost",
    "solace.messaging.service.vpn-name": "default",
    "solace.messaging.authentication.scheme.basic.username": "default",
    "solace.messaging.authentication.scheme.basic.password": "default" }

# Initialize a messaging service 
messaging_service = MessagingService.builder().from_properties(broker_prop).build()
messaging_service.connect()

# Create a reveicer for messages
direct_reveicer = messaging_service\
    .create_direct_message_receiver_builder()\
    .with_subscriptions(topic).build()
direct_reveicer.start()

# Define what the consumer will display when consuming messages
class MessageHandlerImpl(MessageHandler):
    def on_message(self, message: "InboundMessage"):
        print(f"Message: {message}")