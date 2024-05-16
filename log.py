from classes import Logger
import datetime
import pytz
from Discord_Bot import Discord_Bot

class Print_Logger(Logger):
    def log(self, event):
        print (event.__str__())

