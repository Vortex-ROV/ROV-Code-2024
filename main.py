import time
import threading
from src.server_socket import ServerSocket
from src.pixhawk import Pixhawk
from src.oakD import oakServer

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
oak_thread = threading.Thread(target=oakServer.main())
Heeartbeat_thread.start()
oak_thread.start()

while True:
   
    ControlMessage = Sobek.receive(24)

    Sobek.send(pix.get_sensor().encode())

    if ControlMessage is not None:
        pix.ControlPixhawk(ControlMessage)
        print(ControlMessage)

    time.sleep(0.01)
