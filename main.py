from src.server_socket.server_socket import ServerSocket
from src.pixhawk.pixhawk import Pixhawk
import time
import threading
from src.oak_d.baremin import run_camera

from src.server_socket.message import Message

Sobek = ServerSocket(4096)
Sobek.accept()

while True:
    try:
        pix = Pixhawk()
        print("done")
        break
    except:
        print("No pixhawk connected")

Heeartbeat_thread = threading.Thread(target=pix.heartbeat)
# oak_thread = threading.Thread(target=run_camera)
Heeartbeat_thread.start()
# oak_thread.start()

msg_len = len(Message().bytes())

while True:
    
    msg = Sobek.receive(msg_len)

    Sobek.send(pix.get_sensor().encode())

    if msg is not None:
        pix.ControlPixhawk(msg)
        print(msg)

    time.sleep(0.01)
