from datetime import  datetime, timezone
import socket
import sys
import pickle

class Message:
    def __init__(self, sender: str, message: str, time: float, message_type: int):
        self.sender = sender
        self.message = message
        self.time = time
        self.message_type = message_type

class User:
    def __init__(self, name):
        self.name = name

    def send_message(self):
        return pickle.dumps(Message(self.name,
                                    input(f"{datetime.now()} {self.name} || "),
                                    datetime.now().timestamp(),
                                    1 ))

new_user = User("justkamil")
HOST = sys.argv[1]
PORT = 7075 # int(sys.argv[2])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    CONNECTED = True
    s.connect((HOST, PORT))
    while CONNECTED:
        msg = new_user.send_message()
        if msg == b'end':
            CONNECTED = False
        s.sendall(msg)
        data = s.recv(1024)
        parsed_data: Message = pickle.loads(data)
        time: datetime = datetime.fromtimestamp(parsed_data.time, timezone.utc)
        # print(f"{time} {parsed_data.sender} || {parsed_data.message}")
