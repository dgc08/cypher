#!/usr/bin/env python3
from classes import Monitor, Event

from time import time
import uuid
from picamera2 import Picamera2, Preview
from os import getenv

camera = Picamera2()
camera_config = camera.create_still_configuration()
camera.configure(camera_config)

class Camera(Monitor):
    def _get_event(self):
        id = uuid.uuid4()
        filename = getenv("HOME") + "/cypher/images/" + str(id) + ".jpg"

        #camera.start_preview(Preview.QTGL)
        camera.start()
        camera.capture_file(filename)

        return Event(time(), self._id, Event.events.COMPONENT_ACTIVATED, filename)

if __name__ == "__main__":
    cam = Camera("mygog")
    while True:
        input("\nPress enter to take pic")
        print(cam._get_event())
