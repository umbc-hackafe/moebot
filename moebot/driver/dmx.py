from moebot.driver import Driver
import threading
import time

import dmx

DMX_SIZE = 512

FLOW_RATE = .1
SEC_PER_ML = .001


class DmxDriver(Driver):
    def __init__(self, *args, port=None, **kwargs):
        super().__init__()

        if port:
            self.dmx = dmx.DMX_Serial(port)
        else:
            self.dmx = dmx.DMX_Serial()

        self.channels = bytearray(DMX_SIZE)
        self.send()

        self.dmx.start()

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
        self.set_channel(1 + index, int(255 * FLOW_RATE))
        self.send()

        time.sleep(amount * SEC_PER_ML / FLOW_RATE)

        self.set_channel(1 + index, 0)
        self.send()
