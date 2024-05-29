#!/usr/bin/env python3
from classes import Monitor, Event
from time import time
import uuid
from picamera2 import Picamera2, Preview

camera = Picamera2()
camera_config = camera.create_prewiev_configuration()
camera.configure(camera_config)

class Camera(Monitor):
    def _get_event(self):
        id = uuid.uuid4()
        filename = "~/cypher/images/" + str(id) + ".jpg"

        return Event(time(), self._id, Event.events.COMPONENT_ACTIVATED, filename)
