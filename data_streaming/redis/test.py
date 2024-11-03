import redis

# Connect to the Redis server (default localhost:6379)
client = redis.Redis(host="localhost", port=6379, db=0)

# Set a value
client.set("my_key", "Hello, Redis!")

# Get the value
value = client.get("my_key")
print(value.decode("utf-8"))  # Output: Hello, Redis!
