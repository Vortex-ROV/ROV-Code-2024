from src.server_socket.message import Message
import time
import threading
from src.server_socket import ServerSocket
from src.pixhawk import Pixhawk
from src.oakD import oakServer

oak = oakServer()

oak_thread = threading.Thread(target=oak.main)
oak_thread.start()

while True:
    time.sleep(0.01)
