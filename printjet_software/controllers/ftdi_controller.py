from pyftdi.gpio import GpioController, GpioException

class GpioController():
    def __init__(self):
        self._gpio = GpioController()
        self._state = 0

    def open(self, out_pins):
        """Open a GPIO connection, defining which pins are configured as
           output and input"""
        out_pins &= 0xFF
        url = environ.get('FTDI_DEVICE', 'ftdi://ftdi:2232h/1')
        self._gpio.open_from_url(url, direction=out_pins)

    def close(self):
        """Close the GPIO connection"""
        self._gpio.close()

    def set_gpio(self, line, on):
        """Set the level of a GPIO ouput pin.
           :param line: specify which GPIO to madify.
           :param on: a boolean value, True for high-level, False for low-level
        """
        if on:
            state = self._state | (1 << line)
        else:
            state = self._state & ~(1 << line)
        self._commit_state(state)


    def _commit_state(self, state):
        """Update GPIO outputs
        """
        self._gpio.write_port(state)
        # do not update cache on error
        self._state = state
