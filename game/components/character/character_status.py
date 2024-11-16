from components.character.status import Status

from data.logs.logger import logger


class CharacterStatus:
    def __init__(self) -> None:
        self.statuses = {}

    def add_status(self, status: Status):
        self.statuses[status.get_name()] = status

    def get_statuses(self):
        return self.statuses

    def is_empty(self):
        return len(self.statuses) == 0

    def change_duration(self, duration_value: int):
        for status_name, status in self.get_statuses().items():
            status.change_duration(duration_value)

        # Remove expired status
        expired_statuses = {
            status_name: status
            for status_name, status in self.statuses.items()
            if status.is_expired()
        }
        for expired_status_name in expired_statuses.keys():
            logger.debug(f"{expired_status_name} has expired")

        self.statuses = {
            status_name: status
            for status_name, status in self.statuses.items()
            if not status.is_expired()
        }
