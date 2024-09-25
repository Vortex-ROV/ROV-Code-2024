import depthai as dai
from .NetGearServer import NetgearServer
from .OakPipeline import OakPipeline
import threading
import cv2
class oakServer():
    
    def __init__(self, fps=60):
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
        self.video_queue = self.device.getOutputQueue(name="video", maxSize=4, blocking=False)
        self.running = True

        # Start thread for capturing frames from Oak-D
        threading.Thread(target=self._capture_frames, daemon=True).start()
    
    def _capture_frames(self):
        while self.running:
            video_in = self.video_queue.get()
            frame = video_in.getCvFrame()
            # frame = np.ones((1080,1920,3),dtype=np.uint8) * 255
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

    def main(self):
        # Initialize and start the Netgear stream
        
        netgear_stream = oakServer(fps=30)
        netgear_stream.start()

        try:
            while True:
                # Get the latest frame captured by the thread
                frame = netgear_stream.get_latest_frame()
                if frame is not None:
                    # Send the latest frame through the server
                    # netgear_stream.server.send(frame)
                    netgear_stream.server.server.send(frame)

                # Optionally, you can add a small delay or check for exit conditions
                # time.sleep(0.01)
        except :
            print("Exiting...")
            netgear_stream.stop()
            cv2.destroyAllWindows()


    
if __name__ == "__main__":
    camera = oakServer()
    oakServer.main()