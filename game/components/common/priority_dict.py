import heapq


class PriorityDict:
    def __init__(self):
        self.heap = []  # Min-heap to store priorities and keys
        self.entry_map = {}  # Map to store the key-value pairs
        self.counter = 0  # Counter to break ties for elements with the same priority

    def set(self, key, value, priority):
        """Add or update a key with a given value and priority."""
        if key in self.entry_map:
            self.remove(key)  # Remove the old entry
        # Add the new entry to the heap and map
        entry = (priority, self.counter, key, value)
        self.entry_map[key] = entry
        heapq.heappush(self.heap, entry)
        self.counter += 1

    def set_with_highest_priority(self, key, value):
        """Add or update a key with the highest priority (lowest numeric value)."""
        highest_priority = min(self.heap[0][0], 0) if self.heap else 0
        self.set(key, value, highest_priority - 1)

    def get(self, key):
        """Retrieve the value associated with the given key."""
        if key in self.entry_map:
            return self.entry_map[key][3]  # Return the value part of the entry
        raise KeyError(f"Key {key} not found.")

    def has(self, key):
        return key in self.entry_map

    def empty(self):
        return len(self.entry_map) == 0

    def remove(self, key):
        """Remove a key from the priority dictionary."""
        if key in self.entry_map:
            entry = self.entry_map.pop(key)
            # Mark the entry as removed by invalidating its key
            invalid_entry = (entry[0], entry[1], None, None)
            heapq.heappush(self.heap, invalid_entry)

    def get_highest_priority(self):
        """Retrieve the key-value pair with the highest priority."""
        while self.heap:
            priority, _, key, value = heapq.heappop(self.heap)
            if key is not None:  # Skip invalidated entries
                del self.entry_map[key]
                return key, value
        raise KeyError("Priority dictionary is empty.")

    def __contains__(self, key):
        """Check if the key exists in the dictionary."""
        return key in self.entry_map

    def __len__(self):
        """Get the number of valid entries in the dictionary."""
        return len(self.entry_map)
