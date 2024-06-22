from classes import Monitor, Event

from time import time
import socket
import select

HOST = ""
PORT = 6910 # Funny number

class Laser(Monitor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.BUFFER_SIZE = 1024

        # Set up socket for the ESPs to connect to
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # reuseaddr so linux doesn't cry in despair if the program is restarted

        self.server_socket.bind((HOST, PORT))

        self.server_socket.listen(5)
        print('Server listening on port', PORT)

        self.read_list = [self.server_socket]

    def _get_event(self):
        # I copied the read from socket stuff from the web
        # It gathers all the data in recieved_data
        readable, _, _ = select.select(self.read_list, [], [], 0.1)
        received_data = ""
        for s in readable:
            if s is self.server_socket:
                conn, addr = self.server_socket.accept()
                has_data = True
                while has_data:
                    data = conn.recv(self.BUFFER_SIZE).decode('utf-8')
                    if not data:
                        has_data = False
                    received_data += data
                    if '\n' in received_data:
                        has_data = False
            else: # From my understanding, this is useless. But I'm to scared to remove it
                data = s.recv(1024)
                if data:
                    s.send(data)
                else:
                    pass
                self.read_list.remove(s)

        received_data = received_data.strip()
        if received_data == "":
            return None
        elif received_data == "0": # Sender asks for status of tripwire
            if self.get_status():  # Tripwire is on
                conn.send("1".encode('utf-8'))
            else:                  # Tripwire is off
                conn.send("0".encode('utf-8'))
        elif received_data == "1": # The tripwire was activated! Return an event to main
            return Event(time(), self._id, Event.events.COMPONENT_ACTIVATED, received_data.strip())
