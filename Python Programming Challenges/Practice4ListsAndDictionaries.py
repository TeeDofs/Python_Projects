#PRACTICE FOR LISTS AND DICTIONARIES

#List Basics
colors = ["red", "blue", "yellow"]
colors.append("green")
colors.remove("red")


# Dictionary Basics
movie = {
    "title": "Inception",
    "director": "Christopher Nolan",
    "year": 2010,
}
movie["rating"] = 8.8
del movie["year"]


#List Manipulation
numbers = [5, 2, 9, 1, 5, 6]
numbers.sort()
length = len(numbers)


#Dictionary Lookup
def dictionary_lookup():
    students = {
        'Mike': 19, 
        'Anna': 20, 
        'Zoe': 21
    }

    if "Mike" in students:
        print(students["Mike"])
    else:
        print ("Mike not found")

# dictionary_lookup()

#Complex Operation with Lists and Dictionaries
def cost_of_cart():
    products = {'apple': 0.5, 'banana': 0.25, 'cherry': 0.75}
    cart = ['apple', 'banana', 'apple', 'cherry', 'apple', 'cherry']
    total_cost = 0

    for product in cart:
        total_cost += products[product]

    return total_cost

# print(cost_of_cart())