# Basic settings for connectivity 
broker_prop = {
    "solace.messaging.transport.host": "localhost",
    "solace.messaging.service.vpn-name": "default",
    "solace.messaging.authentication.scheme.basic.username": "default",
    "solace.messaging.authentication.scheme.basic.password": "default"}
# Initialize a messaging service 
messaging_service = MessagingService.builder().from_properties(broker_prop).build()
messaging_service.connect()
# Create a publisher for messages and a message
direct_publisher = messaging_service.create_direct_message_publisher_builder().build()
direct_publisher.set_publish_failure_listener(PublishErrorHandling())
direct_publisher.start()
message_body = ''.join(random.choice(string.ascii_letters)for _ in range(32))
outbound_message_builder = messaging_service.message_builder()\
    .with_property("Test", "PA2")\