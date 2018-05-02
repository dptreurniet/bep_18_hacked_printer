import config
from motion_stage_controller import stage_controller




def init():
    print('Starting Initialization...', 'blue')

    stage_ctrl = stage_controller()
    #TODO: init printhead controller

    print('Init succesfull', 'green')



def main_loop():
    print('Main loop started', 'blue')
    pass




if __name__ == '__main__':
    init()
    main_loop()
