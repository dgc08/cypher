from esp_connection import Laser
from log import Print_Logger, Flask_App

loggers = [Print_Logger(), Flask_App()]
monitors = [Laser()]

if __name__ == '__main__':
    pass