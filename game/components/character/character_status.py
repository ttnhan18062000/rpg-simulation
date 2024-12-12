from components.character.status import Status

from data.logs.logger import logger


class CharacterStatus:
    def __init__(self) -> None:
        self.statuses = {}  # StatusClass-Status

    def add_status(self, status: Status):
        status_class = status.get_status_class()
        status_duration = status.get_duration()
        if status_class in self.statuses:
            # Extends the higher level existing status if it has the same class with the new status
            if (
                self.statuses[status_class].get_status_level()
                >= status.get_status_level()
            ):
                logger.debug(
                    f"Extend the {self.statuses[status_class].__class__.__name__} with {status.__class__.__name__} to {status_duration} turns"
                )
                self.statuses[status_class].set_duration(status_duration)
        else:
            logger.debug(
                f"Add new status {status.__class__.__name__} for {status_duration} turns"
            )
            self.statuses[status_class] = status

    def get_statuses(self):
        return self.statuses

    def is_empty(self):
        return len(self.statuses) == 0

    def check_expired_statuses(self):
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

    def change_duration(self, duration_value: int):
        for status_name, status in self.get_statuses().items():
            if status.can_be_expired():
                status.change_duration(duration_value)

        self.check_expired_statuses()

    def recover_debuff(self, duration_value: int):
        for status_name, status in self.get_statuses().items():
            if status.is_debuff() and status.can_be_recovered():
                status.change_duration(duration_value)

        self.check_expired_statuses()

    def has_status_class(self, status_class):
        return status_class in self.statuses

    def __str__(self):
        return " ".join([status.get_name() for status in self.statuses.values()])
