from src.server_socket.message import Message
import time
import threading
from src.server_socket import ServerSocket
from src.pixhawk import Pixhawk
from src.oakD import oakServer

oak = oakServer()
#Sobek = ServerSocket(4096)
#Sobek.accept()

#while True:
    #try:
        #pix = Pixhawk()
        #print("done")
        #break
    #except Exception as e:
        #print(e)
        #print("No pixhawk connected")

#Heeartbeat_thread = threading.Thread(target=pix.heartbeat)
oak_thread = threading.Thread(target=oak.main)
#Heeartbeat_thread.start()
oak_thread.start()

msg_len = len(Message().bytes())

print("Server started")

while True:
    pass
    
    # msg = Sobek.receive(msg_len)

    # Sobek.send(pix.get_sensor().encode())

    # if msg is not None:
        #pix.control_pixhawk(msg)
        #print(msg)

    #time.sleep(0.01)
