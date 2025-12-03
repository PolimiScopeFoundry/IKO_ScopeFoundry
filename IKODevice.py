# -*- coding: utf-8 -*-
"""
Created on fri Mon 24 1:34:36 2025

@authors: Martina Riva. Politecnico di Milano
"""
import SPiiPlusPython as sp
import time
import numpy as np
import sys, socket, struct

class IKO_Device(object):
        '''
    Scopefoundry compatible class to run IKO motors
    '''
        def __init__(self, ip, port, axis):

            #communcation handle
            self.hc = sp.OpenCommEthernetTCP(ip, port)#10.0.0.100

            if self.hc < 0: #0 or >0 means successful connection
                print('Failed to connect')

                self.hc_sim=sp.OpenCommSimulator()
                print(self.hc_sim)
                if self.hc_sim != -1:
                    print('Connected to simulator')
                    self.get_info()
                    connection_list = sp.GetConnectionsList(100, True)
                    
                    for connection in connection_list:
                        print("Connection data:")
                        attributes = dir(connection)
                        custom_attributes = [attr for attr in attributes if not attr.startswith('__')]
                        for attr in custom_attributes:
                            print(f"{attr}: {getattr(connection, attr)}")
                else:            
                    print('Failed to connect to simulator') 
            else:
                print('Connected to controller')
                self.get_info() #all connectons listed: DEBUGGING
                connection_list = sp.GetConnectionsList(100, True)
                print(connection_list)

            self.axis = axis

    
        def get_info(self): #connection info

            IPAddresses = sp.GetEthernetCardsExt(sys.getsizeof(sp.ACSC_APPSL_INFO,
            self.hc), 10, socket.INADDR_BROADCAST, True)
            process_ip = sp.GetConnectionInfo(self.hc, True).EthernetIP
            for ip_addr in IPAddresses:
                ip = socket.inet_ntoa(struct.pack("!L", socket.htonl(int(ip_addr.IpAddress.s_addr))))
                print("Card data:")
                print(f"Controller ip: {ip}")
                print(f"Controller FW version: {ip_addr.Version}")
                print(f"Controller serial number: {ip_addr.SerialNumber}\n\n")


        def get_serial(self):
            SN = sp.GetSerialNumber(self.hc, count = 255, wait = sp.SYNCHRONOUS, failure_check = True)
            return SN 
        
        def getError(self):
            error_code = sp.GetLastError()
            print('Debugging: Error code:', error_code)
            error_str = sp.GetErrorString(self.hc, error_code, 255, failure_check=True)
            print('Error string:',error_str)
      
        def activate(self): #activate the motor
            # if hasattr(self, 'hc_sim'):
            #     sp.Enable(self.hc_sim,0,sp.SYNCHRONOUS,True)
            # else:
                sp.Enable(self.hc,0,sp.SYNCHRONOUS,True)
                print('Debugging: Motor enabled')
                # sp.CommutExt(self.hc, 0, sp.ACSC_NONE,sp.ACSC_NONE, sp.ACSC_NONE, sp.SYNCHRONOUS, True)
                


        def get_timeout(self):
            # if hasattr(self, 'hc_sim'):
            #     return sp.GetTimeout(self.hc_sim, True)
            # else:    
                return sp.GetTimeout(self.hc, True)

        def set_timeout(self, desired_timeout):
            # if hasattr(self, 'hc_sim'):
            #     sp.SetTimeout(self.hc_sim, desired_timeout, True)
            # else:
                sp.SetTimeout(self.hc, desired_timeout, True)


        def Break(self): #terminates motion immediately only if there is a motion planned in the same motion queue
            sp.Break(self.hc, 0, sp.SYNCHRONOUS, True)


        def get_error(self):
            error_code = sp.GetLastError()
            error_str = sp.GetErrorString(self.hc, error_code, 255, failure_check=True)
            print('Debugging: Error code:', error_code)
            print('Debugging: Error string:', error_str)

        def get_velocity(self):
            # if hasattr(self, 'hc_sim'):
            #     return sp.GetVelocity(self.hc_sim, 0, sp.SYNCHRONOUS, True)
            # else:
                return sp.GetVelocity(self.hc, self.axis, sp.SYNCHRONOUS, True)

        def set_velocity(self, desired_velocity):
            # if hasattr(self, 'hc_sim'):
            #     sp.SetVelocity(self.hc_sim, self.axis, desired_velocity, sp.SYNCHRONOUS, True)
            # else:
                sp.SetVelocity(self.hc, self.axis, desired_velocity, sp.SYNCHRONOUS, True)
            #with sp.SYNCHRONOUS the function returns when the controller 
            # response is received.
            #Alternatively: ACSC_WAITBLOCK, IGNORE



        def get_acceleration(self):
            # if hasattr(self, 'hc_sim'):
            #     return sp.GetAcceleration(self.hc_sim, self.axis, sp.SYNCHRONOUS, True)
            # else:
                return sp.GetAcceleration(self.hc, self.axis, sp.SYNCHRONOUS, True)
        
        def set_acceleration(self, desired_acceleration):
            # if hasattr(self, 'hc_sim'):
            #     sp.SetAcceleration(self.hc_sim, self.axis, desired_acceleration, sp.SYNCHRONOUS, True)  
            # else:
                sp.SetAcceleration(self.hc, self.axis, desired_acceleration, sp.SYNCHRONOUS, True)



        def get_deceleration(self):
            # if hasattr(self, 'hc_sim'):
            #     return sp.GetDeceleration(self.hc_sim, self.axis, sp.SYNCHRONOUS, True)
            # else:
                return sp.GetDeceleration(self.hc, self.axis, sp.SYNCHRONOUS, True)
        
        def set_deceleration(self, desired_acceleration):
            # if hasattr(self, 'hc_sim'):
            #     sp.SetDeceleration(self.hc_sim, self.axis, desired_acceleration, sp.SYNCHRONOUS, True)  
            # else:
                sp.SetDeceleration(self.hc, self.axis, desired_acceleration, sp.SYNCHRONOUS, True)



        def get_jerk(self):
            # if hasattr(self, 'hc_sim'):
            #     return sp.GetJerk(self.hc_sim, self.axis, sp.SYNCHRONOUS, True)
            # else:
                return sp.GetJerk(self.hc, self.axis, sp.SYNCHRONOUS, True)
            
        def set_jerk(self, desired_jerk):
            # if hasattr(self, 'hc_sim'):
            #     sp.SetJerk(self.hc_sim, self.axis, desired_jerk, sp.SYNCHRONOUS, True) 
            # else:
                sp.SetJerk(self.hc, self.axis, desired_jerk, sp.SYNCHRONOUS, True)

        #THERE ARE ANALOGOUS FUNCTIONS THAT SET IMMEDIATELY THE VALUE:
        #SetVelocityImm, SetAccelerationImm, SetDecelerationImm, SetJerkImm
        #DO WE NEED THEM?



        def get_fposition(self):#feedback position: a measured position of the motor transferred to user units.
            # if hasattr(self, 'hc_sim'):
            #     return sp.GetFPosition(self.hc_sim, self.axis, sp.SYNCHRONOUS, True)
            # else:
                return sp.GetFPosition(self.hc, self.axis, sp.SYNCHRONOUS, True)
            
        def set_fposition(self, desired_pos): #motor does not move FPOS
            # if hasattr(self, 'hc_sim'):
            #     sp.SetFPosition(self.hc_sim, self.axis, desired_pos, sp.SYNCHRONOUS, True) 
            # else:
                sp.SetFPosition(self.hc, self.axis, desired_pos, sp.SYNCHRONOUS, True)

        def get_fvelocity(self):#feedback velocity FPOS
            # if hasattr(self, 'hc_sim'):
            #     return sp.GetFVelocity(self.hc_sim, self.axis, sp.SYNCHRONOUS, True)    
            # else:
                return sp.GetFVelocity(self.hc, self.axis, sp.SYNCHRONOUS, True)
            
            


        def get_rposition(self):#reference position RPOS
            # if hasattr(self, 'hc_sim'): 
            #     return sp.GetRPosition(self.hc_sim, self.axis, sp.SYNCHRONOUS, True)
            # else:
                return sp.GetRPosition(self.hc, self.axis, sp.SYNCHRONOUS, True)
            
        def set_rposition(self): #motor does not move RPOS:
            # places the origin of the 0 axis to the point where the motor is located this moment(similar to set_home)
            ######## CAN WE NAME THIS FUNCTION SET_HOME???? ##########
            # if hasattr(self, 'hc_sim'): 
            #     sp.SetRPosition(self.hc_sim, 0, desired_pos, sp.SYNCHRONOUS, True)
            # else:       
                sp.SetRPosition(self.hc, self.axis, 0, sp.SYNCHRONOUS, True)
        
        def get_rvelocity(self):#reference velocity
            # if hasattr(self, 'hc_sim'):
            #     return sp.GetRVelocity(self.hc_sim, self.axis, sp.SYNCHRONOUS, True)
            # else:
                return sp.GetRVelocity(self.hc, self.axis, sp.SYNCHRONOUS, True)
            

        def move_absolute(self, desired_pos): #move to a given position
            # if hasattr(self, 'hc_sim'):
            #     sp.ToPoint(self.hc_sim, 0,self.axis, desired_pos, sp.SYNCHRONOUS, True)
            # else:
                sp.ToPoint(self.hc,flags= 0, axis = self.axis, point = desired_pos, wait = sp.SYNCHRONOUS ,failure_check=True)
                #Arguments: handle, flag, axis, position,wait, failure_check
                #flag: 0- start up immediately the motion; 1-  plan the motion but don’t start it until the
                # function Go is executed
                #axis: 0 for axis 1, 1 for axis 2, etc.
        #NOTE: ExtToPoint is available for motion to specified point using the specified velocity or end
        # velocity. MAY IT BE USEFUL?

        def move_relative(self, desired_step):
            # if hasattr(self, 'hc_sim'):
            #     sp.ToPoint(self.hc_sim, sp.MotionFlags.ACSC_AMF_RELATIVE,self.axis, desired_step, sp.SYNCHRONOUS, True)
            # else:
                sp.ToPoint(self.hc, sp.MotionFlags.ACSC_AMF_RELATIVE,self.axis, desired_step, sp.SYNCHRONOUS, True)
 


        def move_sequence(self, step, step_num, start_pos):
            # if hasattr(self, 'hc_sim'):
            #     #the created motion starts only after the first point is specified. 
            #     sp.MultiPoint(self.hc_sim, 0, sp.Axis.ACSC_AXIS_0, 1,failure_check=True)
            #     for i in range(step_num):
            #         sp.AddPoint(self.hc_sim, sp.Axis.ACSC_AXIS_0, start_pos+i*step)
            #         print('Actual position is:',sp.GetRPosition(self.hc_sim, 0, sp.SYNCHRONOUS, True))#debugging
            #     sp.EndSequence(self.hc_sim, sp.Axis.ACSC_AXIS_0)

            # else:
                #the created motion starts only after the first point is specified. 
                sp.MultiPoint(self.hc, 0, self.axis, 1,True)
                for i in range(step_num):
                    sp.AddPoint(self.hc, self.axis, start_pos+i*step)
                sp.EndSequence(self.hc, self.axis)
        #NOTE: this may be a built-in function to perform the scan rather than a for loop.

        # def set_home(self):
            
        # def get_home(self):    

        
        # def go_home(self):

            
        # def gotoRefSwitch(self):
            

        def wait_on_target(self): 
            # if hasattr(self, 'hc_sim'):
            #     sp.WaitMotionEnd(self.hc_sim, 0, sp.SYNCHRONOUS, True)
            # else:
                sp.WaitMotionEnd(self.hc, self.axis, 500, True) # timeout in ms
         
        # def correct_backslash(self, displacement):
        

        # def trigger(self, trigger_step, trigger_stop):
    
        def deactivate(self): #disable motor
            # if hasattr(self, 'hc_sim'):
            #     sp.Disable(self.hc_sim, self.axis, sp.SYNCHRONOUS, True)
            # else:
                sp.Disable(self.hc, self.axis, sp.SYNCHRONOUS, True)


        def stop(self): #terminate a given communication channel
            connection_list = sp.GetConnectionsList(100, True)
            # Terminate last connection
            sp.TerminateConnection(connection_list[-1], True)

        #MAYBE IT IS BETTER TO GIVE THE CONNECTION AS INPUT?

            
        def close(self):
            # Check if hc_sim exists and close it if it does
            # if hasattr(self, 'hc_sim'):
            #     sp.CloseSimulator(failure_check=True)
            #     print('Simulator connection closed')
            # else:
                sp.CloseComm(self.hc, failure_check=False)
                #If True when the function detected an error, it will raise an exception.
                # If False the function will ignore detected errors.
                print('Connection closed')



if __name__=="__main__": 
    
    
    try:
        # Values for ip and port of the controller
        ip="10.0.0.100"
        port= 701
        motor=IKO_Device(ip, port)

        print('Serial number:',motor.get_serial())
        #Settings
        print('Velocity:',motor.get_velocity())
        print('Acceleration:',motor.get_acceleration())

        #Absolute motion
        motor.activate() #motor activation is fundamental
        print('Motor activated')
        print('Initial feedback position:',motor.get_fposition())
        print('Initial reference position:',motor.get_rposition())
        # motor.move_absolute(2.0)
        # motor.wait_on_target() #wait until the motion is completed
        print('Final feedback position:',motor.get_fposition())
        print('Final reference position:',motor.get_rposition())
        motor.deactivate()
        print('Motor deactivated')

        # #Sequence of absolute motions
        # motor.activate()
        # motor.move_sequence(0.1, 10, current_position)
        # motor.deactivate()
        # print('Sequence finished at:',motor.get_fposition())


        # #Relative motion
        # motor.activate()
        # print('Motor activated')
        # print('Initial position:',motor.get_fposition())
        # motor.move_relative(5)
        # print('Final position:',motor.get_fposition())
        # #motor.deactivate()

        #motor.stop()
    finally:
        motor.close()


#REFERENCES:
    #SPiiPlus-Python-Library-Reference-Programmers-Guide.pdf
    #SPiiPlus.NET-Library-Programmers-Guide.pdf
