import cv2
import depthai as dai
import numpy as np
from .NetGearServer import NetgearServer
from .OakPipeline import OakPipeline

class oakServer():
    
    def __init__(self):
        pass
    
    def Main(self):
        # Create the Netgear server
        server =  NetgearServer()
            # Create the Oak pipeline
        pipeline = OakPipeline(FPS=60).get_pipeline()
        # Connect to device and start pipeline
        with dai.Device(pipeline) as device:
            video = device.getOutputQueue(name="video", maxSize=1, blocking=False)
            try:
                while True:
                    videoIn = video.get()
                    server.send(videoIn.getCvFrame())
            except RuntimeError:
                server.close()


if __name__ == "__main__":
    camera = oakServer()
    oakServer.Main()