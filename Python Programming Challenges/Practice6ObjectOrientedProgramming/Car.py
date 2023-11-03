#Car class
class Car:
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year

    def start(self):
        print(f"{self.brand} Starts !!!")

    def stop(self):
        print(f"{self.brand} Stops !!!")

    def honk(self):
        print(f"{self.brand} honkssss !!!")