import heapq

from data.logs.logger import logger


class PriorityDictItem:
    # Allow multiple values of a same key
    def __init__(self, priority, value):
        self.priority = priority
        self.value = value

    def set_priority(self, new_priority):
        self.priority = new_priority

    def get_priority(self):
        return self.priority

    def get_value(self):
        return self.value


class PriorityDict:
    def __init__(self):
        self.dict: dict[str, list[PriorityDictItem]] = {}

    def set(self, priority, key, value):
        new_item = PriorityDictItem(priority, value)
        if key in self.dict:
            self.dict[key].append(new_item)
        else:
            self.dict[key] = [new_item]
        logger.debug(f"Added item {key} to priority dict with priority {priority}")

    def set_with_highest_priority(self, target_key, target_value):
        highest_priority = float("inf")
        for key, values in self.dict.items():
            for value in values:
                cur_priority = value.get_priority()
                if cur_priority < highest_priority:
                    highest_priority = cur_priority
                value.set_priority(cur_priority + 1)
        if highest_priority == float("inf"):
            highest_priority = 1
        self.set(highest_priority, target_key, target_value)
        return highest_priority

    # Push an item to the middle of the priority queue, after a specific priority
    # Push away all the items has lower priority
    def set_to_priority(self, priority, target_key, target_value):
        for key, values in self.dict.items():
            for value in values:
                cur_priority = value.get_priority()
                if cur_priority >= priority:
                    value.set_priority(cur_priority + 2)
        self.set(priority + 1, target_key, target_value)
        return priority + 1

    def get(self, key):
        if key in self.dict:
            return self.dict[key]
        raise KeyError(f"Key {key} not found.")

    def has(self, key, target_value=None):
        if key in self.dict:
            if target_value:
                for value in self.dict[key]:
                    if target_value == value.get_value():
                        return True
            else:
                return True
        return False

    def empty(self):
        return len(self.dict) == 0

    # TODO: Temporary use the priority as unique key to remove element
    def remove_with_priority(self, target_priority):
        for key, values in self.dict.items():
            self.dict[key] = [
                value for value in values if value.get_priority() != target_priority
            ]

    def get_highest_priority(self):
        highest_priority = float("inf")
        highest_priority_value = None
        highest_idx = -1
        highest_key = ""
        for key, values in self.dict.items():
            for idx, value in enumerate(values):
                cur_priority = value.get_priority()
                if cur_priority < highest_priority:
                    highest_priority = cur_priority
                    highest_priority_value = value.get_value()
                    highest_idx = idx
                    highest_key = key

        self.dict[highest_key].pop(highest_idx)
        if len(self.dict[highest_key]) == 0:
            self.dict.pop(highest_key)

        return highest_priority, highest_priority_value

    def __contains__(self, key):
        """Check if the key exists in the dictionary."""
        return key in self.dict

    def __len__(self):
        """Get the number of valid entries in the dictionary."""
        return len(self.dict)
