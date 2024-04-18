class Event:
    # Contains the data for one event, that needs to be loggable
    def __init__(self, timestamp: int, monitor_origin: str, data: str):
        self.timestamp = timestamp
        self.monitor_origin = monitor_origin
        self.data = data

class Monitor:
    # Stuff like the laser or a camera, produces the Events
    def __init__(self, id: str):
        self.__status = False
        self._id = id

    def set_status(self, status: bool):
        self.__status = status

    def get_status(self):
        return self.__status

    def check_for_events(self):
        return self._get_event()

    def _get_event(self):
        return None


class Logger:
    # Stuff like a webserver displaying the events
    def log(self, event: Event):
        pass
