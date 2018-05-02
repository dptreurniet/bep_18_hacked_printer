from pyb import Pin
import config

class stage_controller():
    def __init__(self):
        # Define motion stages
        self.x_stage = stage('x',
                             config.X_STEP,
                             config.X_DIR,
                             config.X_END_MAX,
                             config.X_END_MIN)
         self.x_stage = stage('y',
                              config.Y_STEP,
                              config.Y_DIR,
                              config.Y_END_MAX,
                              config.Y_END_MIN)

        # Define enable pin and disable steppers
        self.stage_ena = Pin(config.STEP_ENA, Pin.OUT_PP)
        self.stage_ena.value(1)

        # Define other properties
        self.range = config.STAGE_RANGE

        print('Stage controller initialized')


    def move_to_position(self, position):
        # Check if target position is within stage range
        if position[0] < 0 or position[0] > self.range[0]:
            return 'target out of range'
        if position[1] < 0 or position[1] > self.range[1]:
            return 'target out of range'


        #TODO: implement movement calculations


class stage():
    def __init__(self, name, p_step, p_dir, p_max, p_min):
        self.name = name

        self.p_step = Pin(p_step, Pin.OUT_PP)
        self.p_dir = Pin(p_dir, Pin.OUT_PP)
        self.p_max = Pin(p_max, Pin.IN)
        self.p_min = Pin(p_min, Pin.IN)

        self.ms = config.STAGE_MICROSTEPPING

        print('stage %s initialized'%(self.name))

    # Functions for checking whether endswitch is triggered
    def at_min(self): return self.p_min.value()
    def at_max(self): return self.p_min.value()

    def step(self, direction):
        # Set direction pin
        self.p_dir.value(direction)

        # Check if endswitch is triggered
        if direction == 1 and self.at_max(): return 'endswitch triggered'
        if direction == 0 and self.at_min(): return 'endswitch triggered'

        # Step
        self.p_step.value(1)
        self.p_step.value(0)

        return True
