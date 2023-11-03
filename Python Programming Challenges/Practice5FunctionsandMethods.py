#PRACTICE FOR FUNCTIONS AND METHODS

#Print Hello World Function
def hello():
    print("Hello World")

#Add numbers function
def add_numbers(a, b):
    return a + b

#Check Even Numbers Function
def is_even(num):
    if(num % 2 == 0):
        return True
    else:
        return False        
    
#Find Longest Word Function
def find_longest_word(word_list):
    longest_word = ""

    for word in word_list:
        if(len(word) > len(longest_word)):
            longest_word = word

    return longest_word

#Calculate Area and Volume of a Sphere
def calculate_area_volume(radius):
    return (4 * 3.14 * (radius**2), ((4/3) * 3.14 * (radius**3)))

#Executions
hello()
print(add_numbers(2, 3))
print(is_even(4))
list_of_words = ["Words", "Can", "Be", "Extremely", "Long"]
print(find_longest_word(list_of_words))
print(calculate_area_volume(3))