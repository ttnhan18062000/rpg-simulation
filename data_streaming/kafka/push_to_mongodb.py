from kafka import KafkaConsumer
import json
from pymongo import MongoClient
import logging
import grpc
import notification_pb2
import notification_pb2_grpc
import time

# Set pymongo logger to WARNING level to suppress DEBUG and INFO logs
logging.getLogger("pymongo").setLevel(logging.WARNING)


def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://nhan:852124@cluster0.qmwjy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    # Create a connection using MongoClient
    client = MongoClient(CONNECTION_STRING)
    # Create the database
    return client["rpgs"]


def insert_or_update_character_by_id(cid, new_char_dict):
    new_values = {"$set": new_char_dict}
    return db["character"].update_one({"id": cid}, new_values, upsert=True)


def notify_nextjs():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = notification_pb2_grpc.NotifierStub(channel)
        response = stub.notifyUpdate(  # Correct method name
            notification_pb2.updateRequest(
                message="New data available"
            )  # Correct message type
        )
        return response.success


# Initialize the database connection
db = get_database()

# Initialize consumer
consumer = KafkaConsumer(
    "rpgs",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",  # Start from the beginning of the topic
    group_id="rpgs_group",
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
)

print("Start data streaming process...")

last_notify_timestamp = time.time()
notify_interval = 1

# Consuming messages
for message in consumer:
    data = message.value
    if data["type"] == "character":
        insert_or_update_character_by_id(data["id"], data)
        # Notify the Next.js server after updating the character data
        if last_notify_timestamp + notify_interval < time.time():
            last_notify_timestamp = time.time()
            notification_success = notify_nextjs()
            if notification_success:
                print("Notification sent successfully to Next.js.")
            else:
                print("Failed to notify Next.js.")


# python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. notification.proto
