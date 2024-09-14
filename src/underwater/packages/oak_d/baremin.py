import cv2
from depthai import Pipeline, Device, ColorCameraProperties
from vidgear.gears import NetGear
import sys

def create_pipeline():
    pipeline = Pipeline()
    cam_rgb = pipeline.createColorCamera()
    cam_rgb.setFps(40)
    xout_rgb = pipeline.createXLinkOut()
    xout_rgb.setStreamName("rgb")
    cam_rgb.preview.link(xout_rgb.input)
    cam_rgb.setPreviewSize(800, 400)
    cam_rgb.setResolution(ColorCameraProperties.SensorResolution.THE_720_P)
    return pipeline

def run_camera():
    # Create Oak-D pipeline
    pipeline = create_pipeline()

    # Start Oak-D pipeline
    with Device(pipeline) as device:
        device.startPipeline()
        out_rgb = device.getOutputQueue("rgb", 1)

        # Open CamGear for sending RGB stream
        options = {"max_retries": sys.maxsize}
        # server = NetGear(
        #     address="192.168.33.101",
        #     port=5555,
        #     protocol="tcp",
        #     pattern=0,
        #     logging=True,
        #     **options
        # )
        server2 = NetGear(
            address="192.168.33.100",
            port=5454,
            protocol="tcp",
            pattern=0,
            logging=True,
            **options
        )

        # Loop to process frames
        while True:
            # Try to get RGB frame
            rgb_in = out_rgb.tryGet()

            # Process RGB frame if available and send it using CamGear
            if rgb_in is not None:
                frame_rgb = rgb_in.getCvFrame()
                # frame_rgb_resized = cv2.resize(frame_rgb, (1920, 1080))
                cv2.imshow("RGB", frame_rgb)
                # server.send(frame_rgb)
                server2.send(frame_rgb)

            # Check for quit command
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Close CamGear server and release resources
    # server.close()
    server2.close()