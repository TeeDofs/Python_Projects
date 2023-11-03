#Fahrenheit To Celsius Function
def fahrenheit_to_celsius(tempF):
    return (tempF - 32) * 5/9

# print("Here is your answer: " , fahrenheit_to_celsius(95))


#Calculate price of materials function
def get_price():
    price = float(input("Enter the price of the product: "))
    amount = int(input("Enter the amount you want: "))

    totalPrice = price * amount

    if(amount > 10):
        totalPrice -= (totalPrice * 0.1)
    
    print("The total price of your purchase is ", format(totalPrice, ".2f"))

# get_price()


#Calculate wage based on hours worked
def calculate_total_wage():
    hours = float(input("Enter the total number of work hours: "))
    rate = float(input("Enter the rate per hour: "))

    if(hours > 40):
        wage = hours * rate * 1.5
    else:
        wage = hours * rate
    print(f"Your total wage is: ${wage:.2f}")

# calculate_total_wage()
