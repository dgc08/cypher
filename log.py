from classes import Logger
import datetime
import pytz

class Print_Logger(Logger):
    def log(self, event):
        print (event.__str__())

class Flask_App(Logger):
    pass
