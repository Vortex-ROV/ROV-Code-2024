import cv2
import depthai as dai
import numpy as np
from NetGearServer import NetgearServer
from OakPipeline import OakPipeline
import threading
import time
class oakServer():
    
    def __init__(self, fps=40):
        self.pipeline = OakPipeline(FPS=fps).get_pipeline()  # Set up the Oak-D pipeline
        self.device = None
        self.video_queue = None
        self.server = NetgearServer()
        self.running = False
        self.latest_frame = None  # Shared resource for the latest frame
        self.frame_lock = threading.Lock()

    def start(self):
        # Start the Oak-D device and stream
        self.device = dai.Device(self.pipeline)
<<<<<<< HEAD
        self.video_queue = self.device.getOutputQueue(name="video", maxSize=2, blocking=False)
=======
        self.video_queue = self.device.getOutputQueue(name="video", maxSize=4, blocking=False)
>>>>>>> 10079d815899b2511d7e27e6465709a380e8eb8f
        self.running = True

        # Start thread for capturing frames from Oak-D
        threading.Thread(target=self._capture_frames, daemon=True).start()
    
    def _capture_frames(self):
        while self.running:
            video_in = self.video_queue.get()
            frame = video_in.getCvFrame()
            # frame = np.ones((1080,1920,3),dtype=np.uint8) * 255
            # print(frame.shape)
            # Store the latest frame with thread safety
            with self.frame_lock:
                self.latest_frame = frame

    def get_latest_frame(self):
        # Return the latest frame in a thread-safe way
        with self.frame_lock:
            return self.latest_frame

    def stop(self):
        self.running = False
        # if self.device is not None:
        #     self.device.close()
        self.server.close()

    def main():
        # Initialize and start the Netgear stream
<<<<<<< HEAD
        start_time_OakServer = time.time()
        netgear_stream = oakServer(fps=40)
        end_time_OakServer = time.time()
        print("Oak Server Init time = ",end_time_OakServer-start_time_OakServer)
=======
        netgear_stream = oakServer(fps=40)
        netgear_stream.start()
>>>>>>> 10079d815899b2511d7e27e6465709a380e8eb8f

        start_time_OakServerStream = time.time()
        netgear_stream.start()
        end_time_OakServerStream = time.time()
        print("Oak Server Stream time = ",end_time_OakServerStream-start_time_OakServerStream)
        try:
            while True:
                # Get the latest frame captured by the thread
                start_time_getf = time.time()
                frame = netgear_stream.get_latest_frame()
                end_time_getf = time.time()
                print("get frame time = ",end_time_getf-start_time_getf)
                if frame is not None:
                    # Send the latest frame through the server
                    start_time_sendf = time.time()
                    netgear_stream.server.send(frame)
                    end_time_sendf = time.time()
                    print("send frame time = ",end_time_sendf-start_time_sendf)
                    # netgear_stream.server.send(frame)

                
                # Optionally, you can add a small delay or check for exit conditions
                # time.sleep(0.01)
        except KeyboardInterrupt:
            print("Exiting...")
            netgear_stream.stop()

if __name__ == "__main__":
    tt = time.time()
    camera = oakServer()
    oakServer.main()
    print("El-Lol = ",time.time()-tt)