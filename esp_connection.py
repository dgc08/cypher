from classes import Monitor, Event

from time import sleep, time
import socket
import select


class Laser(Monitor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        HOST = ""
        PORT = 6910
        self.BUFFER_SIZE = 1024  # Adjust buffer size as needed

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server_socket.bind((HOST, PORT))

        self.server_socket.listen(5)
        print('Server listening on port', PORT)

        self.read_list = [self.server_socket]

    def _get_event(self):
        readable, _, _ = select.select(self.read_list, [], [], 0.1)
        received_data = ''
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
        if received_data.strip() == "":
            return None
        return Event(time(), self._id, received_data.strip())
