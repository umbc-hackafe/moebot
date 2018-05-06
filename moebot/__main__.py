from moebot.driver.dmx2 import DmxDriver
import time


def main():
    driver = DmxDriver(port='/dev/ttyUSB0')

    try:
        while True:
            driver.stop()
            #driver.dispense(0, 1000)
            #time.sleep(1)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()