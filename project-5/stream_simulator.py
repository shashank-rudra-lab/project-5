# stream_simulator.py
from google.cloud import pubsub_v1
import json
import time
import random

# Configuration
PROJECT_ID = "silent-octagon-460701-a0" 
TOPIC_NAME = "stream-topic"
PRODUCTS = ["fan", "table", "chair"]

# Set up Pub/Sub client
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_NAME)

def generate_event():
    return {
        "user_id": random.randint(1, 1000),
        "action": random.choice(["view", "add_to_cart", "purchase"]),
        "product": random.choice(PRODUCTS),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

def publish_events():
    try:
        while True:
            event = generate_event()
            publisher.publish(topic_path, json.dumps(event).encode("utf-8"))
            print(f"Published: {event}")
            time.sleep(5)
    except KeyboardInterrupt:
        print("Stopping publisher...")

if __name__ == "__main__":
    print(f"Simulating events to {TOPIC_NAME}. Press Ctrl+C to stop.")
    publish_events()