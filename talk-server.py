from datetime import datetime, timezone
import socket
import sys
import pickle

from pyasn1.type.useful import UTCTime

HOST = ''
PORT = 7075

class Message:
    def __init__(self, sender: str, message: str, time, message_type):
        self.sender : str = sender
        self.message: str = message
        self.time: float = time
        self.message_type: int = message_type

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    soc.bind((HOST, PORT))
except socket.error as message:
    print('Bind to port failed: ' +  str(message[0]) + "Info: " + message[1])
    sys.exit()


print('socket bound')

soc.listen(9)


conn, addr = soc.accept()

with conn:
    print('Connected with', addr[0] + ":" + str(addr[1]))
    while True:
        data = conn.recv(1024)
        if not data:
            break
        parsed_data : Message = pickle.loads(data)
        time: datetime = datetime.fromtimestamp(parsed_data.time, timezone.utc)
        print(f"{time} {parsed_data.sender} || {parsed_data.message}")
        conn.sendall(pickle.dumps(parsed_data))


