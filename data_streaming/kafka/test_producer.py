from kafka import KafkaProducer
import json
import time

# Initialize producer
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)


# Sending messages to Kafka topic
def produce_messages(topic):
    for i in range(10):
        message = {"number": i, "message": f"Message {i}"}
        producer.send(topic, message)
        print(f"Sent: {message}")
        time.sleep(1)  # Adding a delay to simulate real-time production

    # producer.flush()  # Ensure all messages are sent before closing
    # producer.close()
