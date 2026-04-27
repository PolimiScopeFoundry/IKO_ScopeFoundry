#Simple code for trigger with IKO stage

import time 
import sys
import numpy as np
from IKODevice import IKO_Device

# Values for ip and port of the controller
    #Look for this info in the SpiiPlus App: right click on MyController > Communication parameters > IP address and Port number
ip="10.0.0.100"
port= 701
axis = 0
motor=IKO_Device(ip, port, axis)

print('Serial number:',motor.get_serial())
#Settings
print('Velocity:',motor.get_velocity())
print('Acceleration:',motor.get_acceleration())


motor.activate() #motor activation is fundamental
print('Motor activated')
print('Initial feedback position:',motor.get_fposition())

step=0.01
start_pos=1
step_num=10

positions = np.arange(start_pos, start_pos+step*step_num, step)

motor.trigger(positions, width=1)
# correction = 0.5 #correction to be applied to the position to be sure to be in the trigger range
# motor.move_absolute(1- correction) #Move to a position outside the trigger range to see the effect of the trigger
# motor.wait_on_target() #wait until the motion is completed
try:
    motor.move_absolute(3) #Move to a position outside the trigger range to see the effect of the trigger
    motor.wait_on_target() #wait until the motion is completed
finally:
    motor.trigger_off()

#Closing motor connection
motor.deactivate()
motor.stop()

motor.close()
