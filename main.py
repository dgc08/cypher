from esp_connection import Laser
from log import Print_Logger, Flask_App
from threading import Thread

loggers = [Print_Logger(), Flask_App()]
monitors = [Laser("laser_esp")]

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
            for event in events:
                for logger in loggers:
                    logger.log(event)
