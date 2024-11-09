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


def bulk_insert_or_update_collection_and_notify(collection_type):
    operations = []
    data_list = store_data_for_batch_write[collection_type]
    store_data_for_batch_write[collection_type] = []
    for d in data_list:
        data_action = d.pop("data_action")
        if data_action == "update":
            new_values = {"$set": d}
            operations.append(UpdateOne({"id": d["id"]}, new_values, upsert=True))
        elif data_action == "delete":
            operations.append(DeleteOne({"id": d["id"]}))

    notification_success = notify_nextjs(collection_type)
    if notification_success:
        print("Notification sent successfully to Next.js.")
    else:
        print("Failed to notify Next.js.")
    return db[collection_type].bulk_write(operations)


# Function to run bulk update asynchronously
def run_bulk_update_and_notify_in_thread(data_type):
    if len(store_data_for_batch_write[data_type]) > 0:
        thread = threading.Thread(
            target=bulk_insert_or_update_collection_and_notify,
            args=(data_type,),
        )
        thread.start()


def notify_nextjs(type):
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = notification_pb2_grpc.NotifierStub(channel)
        response = stub.notifyUpdate(  # Correct method name
            notification_pb2.updateRequest(
                message="New data available", type=type
            )  # Correct message type
        )
        return response.success


def flush_batch():
    for data_type in store_data_for_batch_write.keys():
        run_bulk_update_and_notify_in_thread(data_type)


def periodic_flush():
    while not shutdown_flag.is_set():
        time.sleep(flush_interval)
        flush_batch()


# Initialize consumer
def consume_kafka():
    consumer = KafkaConsumer(
        "rpgs",
        bootstrap_servers="localhost:9092",
        auto_offset_reset="earliest",
        group_id="rpgs_group",
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    )
    try:
        while not shutdown_flag.is_set():
            for message in consumer:
                data = message.value
                data_type = data["type"]

                if len(store_data_for_batch_write[data_type]) >= batch_size:
                    run_bulk_update_and_notify_in_thread(data_type)
                else:
                    store_data_for_batch_write[data_type].append(data)
    except Exception as e:
        print(f"Exception in Kafka consumer thread: {e}")
        shutdown_flag.set()  # Signal to shut down
    finally:
        consumer.close()  # Ensure consumer is closed on exit


print("Start data streaming process...")

# Initialize the database connection
db = get_database()

batch_size = 100
flush_interval = 0.5
store_data_for_batch_write = {"character": [], "event": []}

# Flag for clean shutdown
shutdown_flag = threading.Event()


# Main function to start threads and handle shutdown
def main():
    try:
        # Start consumer and flush threads
        consumer_thread = threading.Thread(target=consume_kafka)
        flush_thread = threading.Thread(target=periodic_flush)
        consumer_thread.start()
        flush_thread.start()

        # Wait for threads to finish
        consumer_thread.join()
        flush_thread.join()

    except Exception:
        print("Shutting down...")
        shutdown_flag.set()  # Signal threads to terminate

        # Ensure all threads finish their work
        consumer_thread.join()
        flush_thread.join()


if __name__ == "__main__":
    main()
# python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. notification.proto
