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
        with NetgearServer() as server:
            # Create the Oak pipeline
            pipeline = OakPipeline(FPS=60).get_pipeline()
            # Connect to device and start pipeline
            with dai.Device(pipeline) as device:
                video = device.getOutputQueue(name="video", maxSize=1, blocking=False)
                while True:
                    videoIn = video.get()
                    server.send(videoIn.getCvFrame())

if __name__ == "__main__":
    camera = oakServer()
    oakServer.Main()