# import required libraries
import sys
from vidgear.gears import NetGear


class NetgearServer(NetGear):
    """Creates a tcp Netgear server

    Args:
        IP: IP address of the Netgear server.
        PORT: Port address of the Netgear server.
    """

    def __init__(self, ADDRESS="192.168.33.100", PORT="5454") -> None:
        # define various tweak flags
        options = {
            "jpeg_compression": True,
            "jpeg_compression_quality": 50,
            "jpeg_compression_fastdct": True,
            "jpeg_compression_fastupsample": True,
            # "compression_format": ".png",  # Using PNG format for compression
            # "compression_param": 3,        # Compression level (0 to 9)
            # "max_retries":sys.maxsize
        }
        # Define Netgear Server with default parameters
        # self.server = NetGear(
        #     address=ADDRESS,
        #     port=PORT,
        #     protocol="tcp",
        #     pattern=1,
        #     logging=True,
        #     **options
        # )
        super().__init__(address=ADDRESS,
            port=PORT,
            protocol="tcp",
            pattern=1,
            logging=True,

            **options)
