from email import message
import subprocess
import sys
import random
import string


user_ids = list(range(1, 101))
recipient_ids = list(range(1, 101))


def install_kafka_python():
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "kafka-python"])
    print("kafka-python installed")


def generate_message() -> dict:
    random_user_id = random.choice(user_ids)

    # Copy the recipient array
    recipient_ids_copy = recipient_ids.copy()

    # User can't send message to himself
    recipient_ids_copy.remove(random_user_id)
    random_recipient_id = random.choice(recipient_ids_copy)

    # Generate a random message
    message = ''.join(random.choice(string.ascii_letters)for _ in range(32))

    return {
        'user_id': random_user_id,
        'recipient_id': random_recipient_id,
        'message': message
    }

# install_kafka_python()