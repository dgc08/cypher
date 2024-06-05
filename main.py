#!/usr/bin/env python3

from esp_connection import Laser
from log import Print_Logger, Discord_Bot
from Camera import Camera

from threading import Thread

loggers = [Print_Logger(), Discord_Bot]
monitors = [Laser("laser_esp")]
on_event_logger = [Camera("cam")]

def cons():
    a = input()
    if a=="1" or a=="0":
        if a=="0":
            monitors[0].set_status(False)
        if a=="1":
            monitors[0].set_status(True)
    else:
        print("vergagt")
    cons()

# monitors[0].set_status(False)

if __name__ == '__main__':
    cons_thread = Thread(target=cons)
    cons_thread.start()

    while True:
        events = []
        for i in monitors:
            event = i.check_for_events()
            if event is not None:
                events.append(event)

        if events != []:
            for i in on_event_logger:
                event = i.check_for_events()
                if event is not None:
                    events.append(event)

            for event in events:
                for logger in loggers:
                    logger.log(event)
