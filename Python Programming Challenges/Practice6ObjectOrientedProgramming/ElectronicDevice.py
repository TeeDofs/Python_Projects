#Class for creating and controlling electronic devices
from abc import ABC, abstractmethod

class ElectronicDevice(ABC):
    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass

class Television(ElectronicDevice):
    def __init__(self, control):
        self.control = control

    def turn_on(self):
        self.control = "Push TV Button = TV ON"
        return self.control
    
    def turn_off(self):
        self.control = "Push TV Button again = TV OFF"
        return self.control
    
class Radio(ElectronicDevice):
    def __init__(self, control):
        self.control = control

    def turn_on(self):
        self.control = "Turn Radio knob = RADIO ON"
        return self.control
    
    def turn_off(self):
        self.control = "Turn Radio knob = RADIO OFF"
        return self.control