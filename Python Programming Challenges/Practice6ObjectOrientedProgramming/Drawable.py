#Class of drawable shapes
from abc import ABC, abstractmethod

class Drawable(ABC):
    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def erase(self):
        pass

class Circle(Drawable):
    def __init__(self, shape):
        self.shape = shape

    def draw(self):
        self.shape = "Circle"
        return self.shape

    def erase(self):
        self.shape = ""
        return self.shape
    
class Rectangle(Drawable):
    def __init__(self, shape):
        self.shape = shape

    def draw(self):
        self.shape = "Rectangle"
        return self.shape

    def erase(self):
        self.shape = ""
        return self.shape