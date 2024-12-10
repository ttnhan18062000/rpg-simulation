# from enum import Enum
# import threading


# class WorldNotificationType:
#     class CHARACTER(Enum):
#         DEAD = 1
#         CHANGE_INFO = 2


# class WorldNotificationManager:
#     def __init__(self) -> None:
#         self.listeners = {}

#     def subscribe(self, event_type: WorldNotificationType, callback):
#         if event_type not in self.listeners:
#             self.listeners[event_type] = []
#         self.listeners[event_type].append(callback)

#     def publish(self, event_type, **kwargs):
#         if event_type in self.listeners:
#             for callback in self.listeners[event_type]:
#                 callback(kwargs)


# world_notification_manager = WorldNotificationManager()

# _lock = threading.Lock()


# def get_world_notification_manager():
#     with _lock:
#         return world_notification_manager
