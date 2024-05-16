#!/usr/bin/env python3
from classes import Monitor, Event
from time import time
from random import randint
from picamera2 import Picamera2, Preview

camera = Picamera2()
camera_config = camera.create_prewiev_configuration()
camera.configure(camera_config)

class Camera(Monitor):
    def _get_event(self):
        filename = "~/cypher/images/" + str(randint(1, 2147483647)) + ".jpg"



        return Event(time(), self._id, Event.events.COMPONENT_ACTIVATED, filename)
