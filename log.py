from classes import Logger
import datetime
import pytz

class Print_Logger(Logger):
    def log(self, event):
        print (event.__str__())

class Discord_Bot(Logger):
    pass
