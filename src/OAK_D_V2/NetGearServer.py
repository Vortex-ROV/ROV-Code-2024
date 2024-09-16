# import required libraries
import sys
from vidgear.gears import NetGear


class NetgearServer:
    """Creates a tcp Netgear server

    Args:
        IP: IP address of the Netgear server.
        PORT: Port address of the Netgear server.
    """

    def __init__(self, ADDRESS="192.168.33.100", PORT="5454") -> None:
        # define various tweak flags
        options = {
            "jpeg_compression": True,
            "jpeg_compression_quality": 70,
            "jpeg_compression_fastdct": True,
            "jpeg_compression_fastupsample": True,
        }
        # Define Netgear Server with default parameters
        self.server = NetGear(
            address=ADDRESS,
            port=PORT,
            protocol="tcp",
            pattern=1,
            logging=True,
            **options
        )
