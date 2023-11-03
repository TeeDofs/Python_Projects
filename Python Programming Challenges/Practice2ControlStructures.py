#PRACTICE FOR CONTROL STRUCTURES AND LOOPS

#Display all even numbers from 1 - 20
def display_even_numbers():
    for i in range(1,21):
        if(i%2 == 0):
            print(i)


# display_even_numbers()


#Get sum of all numbers entered
def sum_of_numbers():
    sum_of_num = 0
    stop = False

    while stop == False:
        num = input("Enter a number to add, enter 'stop' to get your answer: ")
        if(num == "stop"):
            stop = True
        else: 
            sum_of_num += int(num)
    
    print(f"Sum of numbers entered is: {sum_of_num}")

# sum_of_numbers()

        
#Display multiplication table
def multiplication_table():
    num = int(input("Enter the number you want the multiplication table of: "))

    print(f"The multiplication table of {num} is ")
    for i in range(1,13):
        print(f"{num} * {i} = {num * i}")

# multiplication_table()

#Display Square of Numbers
def square_numbers():
    num_list = [3, 4, 5, 6, 7, 8, 9]

    for num in num_list:
        print(f"{num} squared = {num * num}")

# square_numbers()


#Get Email Address
def get_email_address():
    email = input("Enter a correct email address: ")

    while "@" not in email or ".com" not in email:
        email = input("Enter a correct email address: ")
    
    print(f"Great! Your email is {email}")

# get_email_address()
     