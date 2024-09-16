from src.server_socket.server_socket import ServerSocket
from src.pixhawk.pixhawk import Pixhawk
import time
import threading
from src.oak_d.baremin import run_camera

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
oak_thread = threading.Thread(target=run_camera)
Heeartbeat_thread.start()
oak_thread.start()

while True:
   
    ControlMessage = Sobek.receive(24)

    Sobek.send(pix.get_sensor().encode())

    if ControlMessage is not None:
        pix.ControlPixhawk(ControlMessage)
        print(ControlMessage)

    time.sleep(0.01)
