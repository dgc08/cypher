from datetime import datetime

import pytz


class Event:
    class events:               # Python doesn't have enums :(
        CHANGE_STATE = 0
        COMPONENT_ACTIVATED = 1
    # Contains the data for one event, that needs to be logged
    def __init__(self, timestamp: float, monitor_origin: str, event_type = events.COMPONENT_ACTIVATED, data: str = ""):
        self.timestamp = timestamp
        self.monitor_origin = monitor_origin
        self.data = data
        self.event_type = event_type

    def event_type_str(self): # For print logger
        if self.event_type == Event.events.COMPONENT_ACTIVATED:
            return "component activated"
        elif self.event_type == Event.events.CHANGE_STATE:
            return "changed state"

    def __str__(self): # For print logger
        def time_format(stamp):
            tz = pytz.timezone("Europe/Berlin")
            dtime = datetime.fromtimestamp(stamp, tz)
            time = dtime.strftime("%H:%M:%S %d.%m.%Y")
            return time

        return f"<{time_format(self.timestamp)}> '{self.monitor_origin}', '{self.event_type_str()}': '{self.data}'"


class Monitor: # Interface for esp_connection
               # For extendability if we want to add more things

    # Stuff like the laser or a camera, produces the Events
    def __init__(self, id: str):
        self.__status = True
        self._id = id

    def set_status(self, status: bool):
        self.__status = status

    def get_status(self):
        return self.__status

    def check_for_events(self):
        return self._get_event()

    def _get_event(self):
        return None


class Logger: # This is practically useless but it looks cool to have an interface for everything
    def log(self, event: Event):
        pass
