import cv2
import depthai as dai
import numpy as np
from NetGearServer import NetgearServer
from OakPipeline import OakPipeline


def main():
    # Create the Netgear server
    server = NetgearServer()
    # Create the Oak pipeline
    pipeline = OakPipeline(FPS=60).get_pipeline()
    # Connect to device and start pipeline
    with dai.Device(pipeline) as device:
        video = device.getOutputQueue(name="video", maxSize=1, blocking=False)
        while True:
            videoIn = video.get()

            # Get BGR frame from NV12 encoded video frame to show with opencv
            # Visualizing the frame on slower hosts might have overhead
            # cv2.imshow("video", cv2.resize(videoIn.getCvFrame(), (1280, 720)))
            server.send(cv2.resize(videoIn.getCvFrame(), (1920, 1080)))
            # if cv2.waitKey(1) == ord('q'):
            #     break
        # print(10000/(time.time()-t))

    # safely close server
    server.close()

if __name__ == "__main__":
    main()