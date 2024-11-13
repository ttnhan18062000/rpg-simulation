from kafka import KafkaProducer
import json

# Initialize producer
# producer = KafkaProducer(
#     bootstrap_servers="localhost:9092",
#     value_serializer=lambda v: json.dumps(v).encode("utf-8"),
# )

# topic = "rpgs"


# Sending messages to Kafka topic
def produce_messages(data):
    return

    producer.send(topic, data)
    # producer.flush()  # Ensure all messages are sent before closing
    # producer.close()
