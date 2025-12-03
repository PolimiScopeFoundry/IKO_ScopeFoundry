# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 16:45:26 2025
@authors: Martina Riva. Politecnico di Milano
"""

from ScopeFoundry import HardwareComponent
from IKODevice import IKO_Device


class IKO_HW(HardwareComponent):
    name = 'IKO_HW'

    def __init__(self, *args, **kwargs):
        if 'ip' in kwargs:
            _ip = kwargs['ip']
            kwargs.pop('ip')
            self._ip = _ip
        else:
            self._ip = '10.0.0.100' 

        if 'port' in kwargs:
            _port = kwargs['port']
            kwargs.pop('port')
            self._port = _port
        else:
            self._port = 701 
        super().__init__(*args, **kwargs)


    def setup(self):
        # create Settings (aka logged quantities)
        self.ip = self.settings.New(name='ip address',dtype=str, initial = self._ip, ro=True)
        self.port = self.settings.New(name='port',dtype=int, initial = self._port, ro=True)
        self.serial = self.settings.New(name='serial',dtype=str, ro=True)  # no serial num initialisation
        self.target_position = self.settings.New(name='target position', dtype=float, unit='mm')
        self.position = self.settings.New(name='position', ro = True, dtype=float, unit='mm', reread_from_hardware_after_write = True)
        
        self.velocity = self.settings.New(name='velocity', dtype=float, unit='mm/s', initial = 0.5, reread_from_hardware_after_write = True)
        self.acceleration = self.settings.New(name='acceleration', dtype=float, unit='mm/s', initial = 0.5, reread_from_hardware_after_write = True)

        self.home = self.settings.New(name='home', dtype=float, unit='mm')
        
        self.add_operation('SetHome', self.set_home)
        self.add_operation('GoHome', self.go_home)
        self.step = self.settings.New(name='step', dtype=float, initial = 5, unit='um')
        self.add_operation('Move', self.move_relative)
        self.add_operation('Stop', self.stop)
        self.add_operation('GotoRefSwitch', self.gotoRefSwitch)
        
        
    def connect(self):
        # connect settings to Device methods
        self.motor = IKO_Device(ip = self._ip,  port = self._port, axis = 0)     
        
        self.serial.hardware_read_func = self.motor.get_serial
        
        self.position.hardware_read_func = self.motor.get_fposition
        self.target_position.hardware_set_func = self.motor.move_absolute
        
        self.velocity.hardware_read_func = self.motor.get_velocity
        self.velocity.hardware_set_func = self.motor.set_velocity     
        self.acceleration.hardware_read_func = self.motor.get_acceleration
        self.acceleration.hardware_set_func = self.motor.set_acceleration 
        
        # self.home.hardware_read_func = self.motor.get_home
        
        self.read_from_hardware()
        
    def disconnect(self):
        if hasattr(self, 'motor'):
            self.motor.close() 
            del self.motor
            
        for setting in self.settings.as_list():
            setting.hardware_read_func = None
            setting.hardware_set_func = None
            
    def set_home(self):
        self.motor.set_rposition()
    
    def stop(self):
        self.motor.stop()
        
    def go_home(self):
        pass

    def move_relative(self):
        self.motor.move_relative(self.step.value)
        self.position.read_from_hardware()
        
    def gotoRefSwitch(self):
        pass
        
        
        
        