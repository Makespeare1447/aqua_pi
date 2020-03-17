import gpiozero as io
from time import sleep

relais_1 = io.LED(pin=20, active_high=False)    #filter
relais_2 = io.LED(pin=21, active_high=False)    #lamp

sleep(1)
relais_1.on()
relais_2.on()
sleep(3)
relais_1.off()
relais_2.off()


print('Success! - you reached the end of the Program!')