#Class for bank account access
#The crux of this method is to protect the internal state of a class by providing access through methods

class BankAccount:
    def __init__(self, balance):
        self.__balance = balance #represents a private attribute

    def deposit(self, amount):
        self.__balance += amount

    def withdraw(self, amount):
        self.__balance -= amount

    def check_balance(self):
        return self.__balance