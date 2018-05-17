from moebot.driver import Driver
import time
import dmx

DMX_SIZE = 512

FLOW_RATE = .5

# Each device in mL/s
DEFAULT_CAL = [50] * 8


class DmxDriver(Driver):
    def __init__(self, *args, port=None, offset=1, calibration=DEFAULT_CAL, **kwargs):
        super().__init__()

        if port:
            self.dmx = dmx.DMX_Serial(port)
        else:
            self.dmx = dmx.DMX_Serial()

        self.channels = bytearray(DMX_SIZE)
        self.send()

        self.calibration = calibration
        self.offset = offset

        self.dmx.start()

        time.sleep(1)
        enable_dmx()

    def set_channel(self, index, val):
        self.channels[index] = min(255, max(0, val))

    def send(self):
        self.dmx.set_data(self.channels)

    def reset(self):
        self.channels = bytearray(DMX_SIZE)

    def stop(self):
        self.reset()
        self.send()
        self.dmx.stop()

    def dispense(self, index, amount):
        self.set_channel(index + self.offset, int(255 * FLOW_RATE))
        self.send()

        time.sleep(amount / self.calibration[index] / FLOW_RATE)

        self.set_channel(index + self.offset, 0)
        self.send()
