#Person Class
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age 

class Student(Person):
    def __init__(self, name, age, grade):
        super().__init__(name, age)  # This calls the __init__ of the Person class
        self.grade = grade