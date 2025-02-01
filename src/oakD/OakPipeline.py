import depthai as dai


class OakPipeline:
    """Defines oak-d pipeline

    Args:
        FPS (int, optional): Frames per second. Defaults
        to 40.

    Returns:
        pipeline: oak-d pipeline

    Functions:
        configure_cameras: sets rgb camera properties and links it with pipeline
        configure_stereo_depth: sets stereo depth properties and links it with pipeline
        configure_post_processing: sets post processing properties for stereo depth
        create_toggle_script: creates a script to toggle between rgb and depth streams
        get_pipeline: connects sources and sinks in oak-d pipeline
        get_stereo: returns stereo depth node in pipeline
    """

    def __init__(self, FPS=40) -> None:
        self.fps = FPS
        # create oak-d pipeline
        self.pipeline = dai.Pipeline()

        # This might improve reducing the latency on some systems
        pipeline.setXLinkChunkSize(0)
        
        self.camRgb = self.pipeline.create(dai.node.ColorCamera)
        # self.camRgb.initialControl.setManualFocus(120)
        self.xoutRgb = self.pipeline.create(dai.node.XLinkOut)

        self.monoLeft = self.pipeline.create(dai.node.MonoCamera)
        self.monoRight = self.pipeline.create(dai.node.MonoCamera)

        self.stereo = self.pipeline.create(dai.node.StereoDepth)

        #Outputs
        self.xoutDepth = self.pipeline.create(dai.node.XLinkOut)
        self.xoutDepth.setStreamName("depth")
        self.xoutDisparity = self.pipeline.create(dai.node.XLinkOut)
        self.xoutDisparity.setStreamName("disparity")
        self.xoutRight = self.pipeline.create(dai.node.XLinkOut)
        self.xoutRight.setStreamName("right")
        
        # Toggle input stream
        self.xinToggle = self.pipeline.create(dai.node.XLinkIn)
        self.xinToggle.setStreamName("toggle")

    def configure_cameras(self):
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

        # Set up mono cameras
        self.monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)
        self.monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
        self.monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)
        self.monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)

    def configure_stereo_depth(self):
        self.stereo.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_ACCURACY)
        self.stereo.initialConfig.setMedianFilter(dai.MedianFilter.KERNEL_7x7)
        self.stereo.setExtendedDisparity(False)
        self.stereo.setLeftRightCheck(True)
        self.stereo.setSubpixel(True)
        
        self.monoLeft.out.link(self.stereo.left)
        self.monoRight.out.link(self.stereo.right)
        self.stereo.depth.link(self.xoutDepth.input)
        self.stereo.disparity.link(self.xoutDisparity.input)
        self.monoRight.out.link(self.xoutRight.input)
    
    def configure_post_processing(self):
        config = self.stereo.initialConfig.get()
        config.postProcessing.speckleFilter.enable = False
        config.postProcessing.speckleFilter.speckleRange = 50
        config.postProcessing.temporalFilter.enable = True
        config.postProcessing.spatialFilter.enable = True
        config.postProcessing.spatialFilter.holeFillingRadius = 10
        config.postProcessing.spatialFilter.numIterations = 1
        config.postProcessing.thresholdFilter.minRange = 400
        config.postProcessing.thresholdFilter.maxRange = 15000
        config.postProcessing.decimationFilter.decimationFactor = 1
        self.stereo.initialConfig.set(config)
        self.stereo.setDepthAlign(dai.CameraBoardSocket.CAM_C)

    def create_toggle_script(self):
        script = self.pipeline.create(dai.node.Script)
        script.setScript("""
            toggle = False
            while True:
                msg = node.io['toggle'].tryGet()
                if msg:
                    toggle = not toggle
                    node.warn('Toggled! Current pipeline: ' + ('Depth' if toggle else 'RGB'))

                if toggle:
                    depth = node.io['depth'].tryGet()
                    disparity = node.io['disparity'].tryGet()
                    right = node.io['right'].tryGet()
                    if depth: node.io['depth_out'].send(depth)
                    if disparity: node.io['disparity_out'].send(disparity)
                    if right: node.io['right_out'].send(right)
                else:
                    rgb = node.io['rgb'].tryGet()
                    if rgb: node.io['rgb_out'].send(rgb)
        """)

        self.camRgb.video.link(script.inputs['rgb'])
        self.stereo.depth.link(script.inputs['depth'])
        self.stereo.disparity.link(script.inputs['disparity'])
        self.monoRight.out.link(script.inputs['right'])
        self.xinToggle.out.link(script.inputs['toggle'])

        script.outputs['rgb_out'].link(self.xoutRgb.input)
        script.outputs['depth_out'].link(self.xoutDepth.input)
        script.outputs['disparity_out'].link(self.xoutDisparity.input)
        script.outputs['right_out'].link(self.xoutRight.input)
    
    def get_stereo(self):
        return self.stereo

    def get_pipeline(self):
        """connects sources and sinks in oak-d pipeline

        Returns:
            pipeline: oak-d pipeline
            max_disparity: maximum disparity of depth map
        """
        self.configure_cameras()
        self.configure_stereo_depth()
        self.configure_post_processing()
        self.create_toggle_script()
        pipeline = self.pipeline
        return pipeline