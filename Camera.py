#!/usr/bin/env python3
from classes import Monitor, Event

from time import time
import uuid
from picamera2 import Picamera2, Preview
from os import getenv

camera_there = True
try:
    camera = Picamera2()
    camera_config = camera.create_still_configuration()
    camera.configure(camera_config)
except:
    camera_there = False # Make sure the program also works if there is no camera connected

class Camera(Monitor):
    # If get event is called, we WANT an image
    def _get_event(self):
        id = uuid.uuid4() # random id for filename
        filename = getenv("HOME") + "/cypher/images/" + str(id) + ".jpg"

        if camera_there:
            #camera.start_preview(Preview.QTGL)
            camera.start()
            camera.capture_file(filename)

            return Event(time(), self._id, Event.events.COMPONENT_ACTIVATED, filename)

# To test the camera
if __name__ == "__main__":
    cam = Camera("some camera")
    while True:
        input("\nPress enter to take pic")
        print(cam._get_event())
