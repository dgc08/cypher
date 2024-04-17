from classes import Monitor, Event

from time import sleep, time

class Laser(Monitor):
    def _get_event(self):
        sleep(1)
        return Event(time(), self._id, "test")
