# Written by Daan Treurniet

# This is the main controller of the printjet system,
# which controls all aspects of the printer


from motion_stage_controller import MotionStageController
from printhead_controller import PrintheadController


class MainController():
    def __init__(self):
        self.motion_stage_controller = MotionStageController()
        self.printhead_controller = PrintheadController()
        print('Main Controller initialized...')

    def main_loop(self):
        pass



if __name__ == '__main__':
    main_controller = MainController()
    main_controller.main_loop()
