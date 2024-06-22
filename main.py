#!/usr/bin/env python3

# Guten Tag

from esp_connection import Laser
from log import Print_Logger, Discord_Bot
from Camera import Camera

from threading import Thread

monitors = [Laser("laser_esp")] # Takes care of both ESPs
loggers = [Print_Logger(), Discord_Bot(monitors[0].set_status)] # Two loggers: One that just prints stuff and the discord bot
                                                                # The discord bot needs a method to turn off the tripwire

on_event_logger = [Camera("cam")]                               # On event logger are monitors that only log if the other monitors give a signal

# Only for testing use !activate and !deactivate on the discord bot
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
    cons_thread = Thread(target=cons) # you could turn off the tripwire from the console if you'd want (not recommended)
    cons_thread.start()

    while True:
        events = []
        for i in monitors:                  # For every monitor (only tripwire for now)
            event = i.check_for_events()
            if event is not None:
                events.append(event)        # Save event if there is one

        if events != []:                    # If there are events,
            for i in on_event_logger:       # gather events from the on_event_loggers (only cam for now)
                event = i.check_for_events()
                if event is not None:
                    events.append(event)

            for event in events:            # and log all events
                for logger in loggers:
                    logger.log(event)
