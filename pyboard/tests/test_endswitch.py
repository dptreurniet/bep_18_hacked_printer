import pyb
import time

end_sw = pyb.Pin('X1', pyb.Pin.IN)

while True:
    print(end_sw.value())
    time.sleep(0.01)
