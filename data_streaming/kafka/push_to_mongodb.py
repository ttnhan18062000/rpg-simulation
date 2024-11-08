from kafka import KafkaConsumer
import json
from pymongo import MongoClient, UpdateOne, DeleteOne
import logging
import grpc
import notification_pb2
import notification_pb2_grpc
import time
import threading

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


def insert_or_update_combat_by_id(cid, new_combat_dict):
    new_values = {"$set": new_combat_dict}
    return db["combat"].update_one({"id": cid}, new_values, upsert=True)


def bulk_insert_or_update_collection(data_list, collection_type):
    operations = []
    for d in data_list:
        data_action = d.pop("data_action")
        if data_action == "update":
            new_values = {"$set": d}
            operations.append(UpdateOne({"id": d["id"]}, new_values, upsert=True))
        elif data_action == "delete":
            operations.append(DeleteOne({"id": d["id"]}))
    return db[collection_type].bulk_write(operations)


def notify_nextjs(type):
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = notification_pb2_grpc.NotifierStub(channel)
        response = stub.notifyUpdate(  # Correct method name
            notification_pb2.updateRequest(
                message="New data available", type=type
            )  # Correct message type
        )
        return response.success


def check_timestamp_for_notification_type(data_type, timestamp_now):
    # Notify the Next.js server after updating the character data
    if last_notify_timestamp[data_type] + notify_interval < timestamp_now:
        last_notify_timestamp[data_type] = timestamp_now
        notification_success = notify_nextjs(data_type)
        if notification_success:
            print("Notification sent successfully to Next.js.")
        else:
            print("Failed to notify Next.js.")


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

last_notify_timestamp = {"character": time.time(), "event": time.time()}
notify_interval = 1

last_update_timestamp = {"character": time.time(), "event": time.time()}
update_interval = 0.1

store_data_for_batch_write = {"character": [], "event": []}

# Function to run bulk update asynchronously
def run_bulk_update_in_thread(data_list, data_type):
    thread = threading.Thread(
        target=bulk_insert_or_update_collection,
        args=(
            data_list,
            data_type,
        ),
    )
    thread.start()


# Consuming messages
for message in consumer:
    data = message.value
    data_type = data["type"]
    now = time.time()

    # Check if we need to update this data type
    if last_update_timestamp[data_type] + update_interval < now:
        # Launch a thread to perform bulk update for this data_type
        if len(store_data_for_batch_write[data_type]) > 0:
            run_bulk_update_in_thread(store_data_for_batch_write[data_type], data_type)
            store_data_for_batch_write[data_type] = []
        last_update_timestamp[data_type] = now
    else:
        # Store data to batch update
        store_data_for_batch_write[data_type].append(data)

    # Check for notifications (assuming this is another function)
    check_timestamp_for_notification_type(data_type, now)


# python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. notification.proto
