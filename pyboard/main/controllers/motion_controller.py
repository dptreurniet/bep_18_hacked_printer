import pyb

class MotionController():
    def __init__(self):
        self.x_stage = Stage()
        self.y_stage = Stage()

class Stage():
    '''
    Motion Stage Class to control movement of a 1D motion stage
    Implements the use of a A4988 stepper driver with optional microstepping
    '''
    def __init__(pin_step, pin_dir, pin_enable, steps_per_rev=200, microstepping=8):
        self.pin_step = pyb.Pin(pin_step, pyb.Pin.OUT_PP)
        self.pin_dir = pyb.Pin(pin_dir, pyb.Pin.OUT_PP)
        self.pin_enable = pyb.Pin(pin_enable, pyb.Pin.OUT_PP)

        self.steps_per_rev = steps_per_rev
        self.ms = microstepping

        self.reverse = False
        self.hard_stop = False

    def __set_dir(self, direction):
        if direction == 1:
            if self.reverse: self.pin_dir.value(1)
            else: self.pin_dir.value(0)
        else:
            if self.reverse: self.pin_dir.value(0)
            else: self.pin_dir.value(1)
        return True

    def set_hardstop(self, hardstop):
        self.hardstop = hardstop
        return True

    def step(self, direction):
        # Set direction pin of the stepper driver
        self.__set_dir(direction)

        # Enable stepper driver
        self.pin_enable.value(1)

        # Pulse step pin
        self.pin_step.value(1)
        pyb.delay(1)
        self.pin_step.value(0)

        # If soft stop, release enable pin
        if !self.hard_stop: self.pin_enable.value(0)

        return True
