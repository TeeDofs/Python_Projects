#PRACTICE ON ARRAYS

#Function to calculate sum of numbers in a list
def list_sum(our_list):
    our_sum = 0
    for num in our_list:
        our_sum += num

    return our_sum

#Function to find the highest and lowest numbers in an array 
def min_max(our_list):
    return min(our_list), max(our_list)

#Function to find and return the index of an item in a list
def find_item_index(item, our_list):
    if item in our_list:
        return our_list.index(item)
    else:
        return -1
    

#Function to reverse an array
def reverse_list(our_list):
    return list(reversed(our_list))

#Function to remove duplicates from an array
def remove_duplicates(our_list):
    return list(set(our_list))

#Execution
new_list = [3, 2, 2, 1, 4, 5]
print(list_sum(new_list))
print(min_max(new_list))
print(find_item_index(1, new_list))
print(reverse_list(new_list))
print(remove_duplicates(new_list))