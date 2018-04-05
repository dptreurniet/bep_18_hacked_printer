import operator
from math import sqrt
import matplotlib.pyplot as plt

class MotionStageController():
    """
    This class takes care of controller the motion stage.
    """

    #TODO implement hard limits (switches)
    #TODO implement soft limits

    def __init__(self):
        self.x_stage = Stage('x_stage', 200, 1, 26, 8, 9, 1)
        self.y_stage = Stage('y_stage', 200, 1, 26, 8, 9, 1)

        self.log_goals = []

        self.pos = [0, 0]
        print('Motion Stage Controller initialized...')

    def home_stage(self, stage):
        if stage=='x':
            self.x_stage.home()
            return True
        if stage=='y':
            self.y_stage.home()
            return True
        else: return False

    def home_stages(self):
        self.home_stage('x')
        self.home_stage('y')
        return True

    def move_to_position(self, position, log=True, debug=False):
        if log: print('\nStarting move_to_position from %s to %s'%(self.pos, position))
        self.log_goals.append(position)
        position = [float(i) for i in position]
        [dx, dy] = list(map(operator.sub, position, self.pos))
        dirs = [sign(dx), sign(dy)]
        if debug: print('dirs: %s'%(dirs))

        try:
            goal_slope = dy/dx
        except ZeroDivisionError: goal_slope = 1000000000
        if debug: print('goal_slope: %s'%(goal_slope))

        start_pos = self.pos[:]

        max_steps_x = ((self.x_stage.range/self.x_stage.leadscrew_pitch)*self.x_stage.steps_per_rev)
        max_steps_y = ((self.y_stage.range/self.y_stage.leadscrew_pitch)*self.y_stage.steps_per_rev)

        step_counter = 0
        while True:
            # Check wether it possible to get closer
            if (abs(position[0] - self.pos[0])<=(self.x_stage.stepsize)/2.0 and
                abs(position[1] - self.pos[1])<=(self.y_stage.stepsize)/2.0):
                diff_x = self.pos[0]-position[0]
                diff_y = self.pos[1]-position[1]
                if log: print("Exited move_to_position normally with dx=%s, dy=%s"%(diff_x, diff_y))
                #self.pos = position
                return True

            # Check if the max number of steps is not exceeded
            if step_counter > max(max_steps_x, max_steps_y):
                print("\nWarning: Stopped move_to_position because max steps exceeded.")
                return False



            step_x, step_y = False, False
            # Determine best option: step only X, only Y or both
            # This is done by comparing the goal_slope to the resulting slope after stepping
            try:
                slope1 = ((self.pos[1]-start_pos[1]) /
                (self.pos[0]+dirs[0]*self.x_stage.stepsize-start_pos[0]))
            except ZeroDivisionError: slope1 = 1000000000

            try:
                slope2 = ((self.pos[1]+dirs[1]*self.y_stage.stepsize-start_pos[1]) /
                (self.pos[0]-start_pos[0]))
            except ZeroDivisionError: slope2 = 1000000000

            try:
                slope3 = ((self.pos[1]+dirs[1]*self.y_stage.stepsize-start_pos[1]) /
                (self.pos[0]+dirs[0]*self.x_stage.stepsize-start_pos[1]))
            except ZeroDivisionError: slope3 = 1000000000

            possible_slopes = map(abs, [slope1-goal_slope, slope2-goal_slope, slope3-goal_slope])
            if debug: print('possible_slopes: %s'%([slope1, slope2, slope3]))

            best_option = possible_slopes.index(min(possible_slopes))
            if debug: print('best_option: %s'%(best_option))
            if best_option == 0: step_x = True
            if best_option == 1: step_y = True
            if best_option == 2: step_x, step_y = True, True

            # Exectute stepping
            self.x_stage.step(dirs[0], step_x)
            self.y_stage.step(dirs[1], step_y)

            self.pos = [self.x_stage.pos, self.y_stage.pos]
            step_counter += 1

    def plot_log(self):
        log_pos_x = []
        log_pos_y = []

        plt.plot(self.x_stage.log, self.y_stage.log)

        x_data = [self.log_goals[i][0] for i in range(len(self.log_goals))]
        y_data = [self.log_goals[i][1] for i in range(len(self.log_goals))]

        plt.scatter(x_data, y_data, c='r')
        plt.show()

    def clear_log(self):
        self.x_stage.clear_log()
        self.y_stage.clear_log()
        self.log_goals = []





class Stage():
    def __init__(self, name, steps_per_rev, leadscrew_pitch, motion_range, pin_dir, pin_step, ms=1):
        self.name = name

        self.steps_per_rev = steps_per_rev
        self.leadscrew_pitch = leadscrew_pitch

        self.range = motion_range
        self.soft_padding = 0

        self.pin_dir = pin_dir
        self.pin_step = pin_step

        self.ms = ms #microstepping

        self.stepsize = float(self.leadscrew_pitch) / float(self.steps_per_rev)
        self.pos = 0
        self.is_homed = False
        self.log = []

    def step(self, direction, step, disable_softstop=False):
        if step:
            new_pos = self.pos+direction*self.stepsize
            if ((new_pos < self.range-self.soft_padding and new_pos > self.soft_padding) or
                disable_softstop):
                self.pos += direction*self.stepsize
                # TODO: implement step with direction
            #print('Stepping %s'%(self.name))
        self.log.append(self.pos)
        return True

    def clear_log(self): self.log = []

    def home(self):
        #TODO move stage until limit switch is triggered
        self.pos = 0
        #TODO move stage inside soft boundaries
        self.is_homed = True
        return True





def sign(i):
    if i<0: return -1
    return 1
