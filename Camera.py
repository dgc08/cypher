#!/usr/bin/env python3
from classes import Monitor, Event
from time import time

class Camera(Monitor):
    def _get_event(self):
        return Event(time(), self._id, Event.events.COMPONENT_ACTIVATED, )
