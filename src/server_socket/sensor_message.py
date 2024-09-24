from . import Message

class SensorMessage(Message):
    def __init__(self, msg=b"") -> None:
        self._msg = {
            "pressure": 0.0,
            "temperature": 0.0,
            "depth": 0.0,
            "heading": 0
        }

        self.recreate_msg(msg)


def main():
    msg = SensorMessage()
    msg.set_value("pressure", 5.0)
    msg2 = SensorMessage(msg.bytes())

    print(msg)
    print(msg2)

if __name__ == "__main__":
    main()