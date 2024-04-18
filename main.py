from esp_connection import Laser
from log import Print_Logger, Flask_App

loggers = [Print_Logger(), Flask_App()]
monitors = [Laser("laser_esp")]

if __name__ == '__main__':
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
