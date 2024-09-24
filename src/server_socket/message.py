import unittest
import struct


class Message:
    """
    Class for abstracting the message sent from the TCU to the ROV companion computer
    """

    def __init__(self, msg=b"") -> None:
        # default message
        self._msg = {
            "throttle": 1500,
            "yaw": 1500,
            "forward": 1500,
            "lateral": 1500,
            "gripper_1": False,
            "gripper_2": False,
            "light": "0",
            "rotating_gripper": "O",
            "armed": False,
            "flight_mode": "M",
            "joystick_connect": False,
        }

        self.recreate_msg(msg)

    def recreate_msg(self, msg: bytes) -> None:
        if msg == b"":
            return

        index = 0
        for key in self._msg.keys():
            if isinstance(self._msg[key], int):
                self._msg[key] = int.from_bytes(msg[index : index + 4], "big")
                index += 4
            elif isinstance(self._msg[key], float):
                self._msg[key] = struct.unpack("d", msg[index : index + 8])[0]
                index += 8
            elif isinstance(self._msg[key], str):
                self._msg[key] = "".join(
                    map(chr, msg[index : index + len(self._msg[key])])
                )
                index += len(self._msg[key])
            elif isinstance(self._msg[key], bool):
                self._msg[key] = bool.from_bytes(msg[index], "big")
                index += 1
            else:
                raise Exception("Unrecognised data type")

    def bytes(self) -> bytes:
        """
        Get the bytes representation of the message to be sent through the socket
        """
        b = b""
        for key in self._msg.keys():
            if isinstance(self._msg[key], int):
                b += self._msg[key].to_bytes(4, "big")
            elif isinstance(self._msg[key], float):
                b += struct.pack("d", self._msg[key])
            elif isinstance(self._msg[key], str):
                b += self._msg[key].encode()
            elif isinstance(self._msg[key], bool):
                b += self._msg[key].to_bytes(1, "big")
            else:
                raise Exception("Unrecognised data type")
        return b

    def get_value(self, key):
        """
        Get the value of a key from the message dictionary
        """
        return self._msg[key]

    def set_value(self, key, value) -> None:
        """
        Set the value of a key in the message dictionary

        ### Notes:
            - Can not create new keys in the dictionary
            - Can only override message values with values of the same type
            - Can only override string type message values with those of the same length
        """
        if (
            key in self._msg
            and type(self._msg[key]) == type(value)
            and (
                type(value) == str
                and len(value) == len(self._msg[key])
                or type(value) != str
            )
        ):
            self._msg[key] = value
        else:
            raise ValueError()

    def __eq__(self, value) -> bool:
        return self._msg == value.__msg

    def __str__(self) -> str:
        return str(self._msg)


class Test(unittest.TestCase):
    def test_msg(self):
        encoded_msg = Message()

        encoded_msg.set_value("throttle", 1600)
        encoded_msg.set_value("yaw", 1600)
        encoded_msg.set_value("forward", 1400)
        encoded_msg.set_value("lateral", 1200)

        encoded_msg.set_value("gripper_1", True)
        encoded_msg.set_value("gripper_2", False)
        encoded_msg.set_value("light", "H")
        encoded_msg.set_value("rotating_gripper", "L")

        encoded_msg.set_value("armed", True)
        encoded_msg.set_value("flight_mode", "S")
        encoded_msg.set_value("joystick_connect", True)

        decoded_msg = Message(encoded_msg.bytes())
        self.assertEqual(decoded_msg, encoded_msg)


if __name__ == "__main__":
    unittest.main()
