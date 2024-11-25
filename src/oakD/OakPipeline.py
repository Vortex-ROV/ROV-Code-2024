import depthai as dai


class OakPipeline:
    """Defines oak-d pipeline

    Args:
        FPS: rate at which camera should produce frames
        COLOR_DIM: dimension of color camera
        DEPTH_POST_PROCESSING: flag that enables depth post processing

    Attributes:
        fps = rate at which camera should produce frames
        depth_post_processing: flag that enables depth post processing
        color_dim: dimension of color camera
        pipeline: oak-d pipeline
        camRgb: color camera node
        monoRight: right camera node
        monoLeft: left camera node
        xoutRgb: color camer output
    """

    def __init__(self, FPS=40) -> None:
        self.fps = FPS
        # create oak-d pipeline
        self.pipeline = dai.Pipeline()

        # This might improve reducing the latency on some systems
        # self.pipeline.setXLinkChunkSize(0)
        
        self.camRgb = self.pipeline.create(dai.node.ColorCamera)
        # self.camRgb.initialControl.setManualFocus(120)
        self.xoutRgb = self.pipeline.create(dai.node.XLinkOut)

        
    def color_camera_properties_linking(self):
        """sets rgb camera properties and links it with pipeline"""

        # Properties
        self.camRgb.setBoardSocket(dai.CameraBoardSocket.CAM_A)
        self.camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_4_K)
        self.camRgb.setPreviewSize(1920, 1080)
        self.camRgb.setIspScale(1,2)
        self.camRgb.setFps(self.fps)
        
        # Linking
        self.xoutRgb.setStreamName("video")
        self.xoutRgb.input.setBlocking(False)
        self.xoutRgb.input.setQueueSize(4)
        self.camRgb.video.link(self.xoutRgb.input)


    
    def get_pipeline(self):
        """connects sources and sinks in oak-d pipeline

        Returns:
            pipeline: oak-d pipeline
            max_disparity: maximum disparity of depth map
        """
        self.color_camera_properties_linking()
        pipeline = self.pipeline
        return pipeline


