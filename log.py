from classes import Logger
import datetime
import pytz

def time_format(stamp):
    tz = pytz.timezone("Europe/Berlin")
    dtime = datetime.datetime.fromtimestamp(stamp, tz)
    time = dtime.strftime("%H:%M:%S %d.%m.%Y")
    return time


class Print_Logger(Logger):
    def log(self, event):
        print (f"<{time_format(event.timestamp)}> '{event.monitor_origin}' send '{event.data}'")

class Flask_App(Logger):
    pass
