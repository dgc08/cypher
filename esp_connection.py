from classes import Monitor, Event

from time import time
import socket
import select

HOST = ""
PORT = 6910

class Laser(Monitor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.BUFFER_SIZE = 1024

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.server_socket.bind((HOST, PORT))

        self.server_socket.listen(5)
        print('Server listening on port', PORT)

        self.read_list = [self.server_socket]

    def _get_event(self):
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
            else:
                data = s.recv(1024)
                if data:
                    s.send(data)
                else:
                    pass
                self.read_list.remove(s)

        received_data = received_data.strip()
        if received_data == "":
            return None
        elif received_data == "0":
            if self.get_status():
                conn.send("1".encode('utf-8'))
            else:
                conn.send("0".encode('utf-8'))
        elif received_data == "1":
            return Event(time(), self._id, Event.events.COMPONENT_ACTIVATED, received_data.strip())
