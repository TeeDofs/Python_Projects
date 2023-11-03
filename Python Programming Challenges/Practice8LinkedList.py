#PRACTICE FOR LINKED LIST

#Create the individual node element. It consists of two parts - The data and the next pointing to the next node
class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedList: 
    def __init__(self):
        self.head = None

    #Add to the end of the list
    def append(self, data):
        new_node = Node(data)

        if not self.head:
            self.head = new_node
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node

    #Display the current list
    def display(self):
        curr_node = self.head
        while curr_node:
            print(curr_node.data, end=" -> ")
            curr_node = curr_node.next
        print("None")

    #Insert element at the start of list
    def insert_element_at_start(self, element):
        new_node = Node(element)
        new_node.next = self.head
        self.head = new_node

    #Insert element after the C element
    def insert_after_element(self, element, inserted_element):
        curr_node = self.head
        while curr_node:
            if(curr_node.data == element):
                sec_node = Node(inserted_element)
                sec_node.next = curr_node.next
                curr_node.next = sec_node

            curr_node = curr_node.next

    #Remove first occurrence of "B"
    def remove_first_occurrence(self, element):
        curr_node = self.head
        prev_node = None

        while curr_node:
            if curr_node.data == element:
                if prev_node:
                    prev_node.next = curr_node.next
                    curr_node = curr_node.next
                    continue
                else:
                    self.head = curr_node.next
                    curr_node = self.head
                    continue
            prev_node = curr_node
            curr_node = curr_node.next

    #Remove the 4th item in the list
    def remove_item_at_num(self, num):
        curr_node = self.head
        prev_node = None
        index = 0
        while curr_node:
            if index == num - 1:
                prev_node.next = curr_node.next
                curr_node = curr_node.next
            index += 1
            prev_node = curr_node
            curr_node = curr_node.next

    #Check if an element exists in the list 
    def check_if_element_exists(self, element):
        curr_node = self.head
        index = 0

        while curr_node:
            if curr_node.data == element:
                print(f"The node exists at position {index+1} ")
                return index
            index += 1
            curr_node = curr_node.next

        print("Element does not exist in the list")

    #NEEDS MORE STUDYING - DO NOT FULLY UNDERSTAND CONCEPT YET #############
    #Reverse the linked list
    def reverse(self):
        prev_node = None
        curr_node = self.head

        while curr_node:
            next_node = curr_node.next
            curr_node.next = prev_node
            prev_node = curr_node
            curr_node = next_node
        self.head = prev_node

    #Find the middle of the list
    def find_middle(self):
        curr_node = self.head
        index = 0

        while curr_node:
            curr_node = curr_node.next
            index+=1
        index_count = index
        middle = index_count//2

        curr_node = self.head
        index = 0

        while curr_node:
            if(index == middle):
                if index_count % 2 != 0:
                    return curr_node.data
                else:
                    return curr_node.data, curr_node.next.data
                
            curr_node = curr_node.next
            index += 1

    #Check if the list has a loop
    def check_loop(self):
        tortoise = self.head
        hare = self.head

        #Move through list with hare moving 2x speed of tortoise
        while hare is not None and hare.next is not None:
            tortoise = tortoise.next
            hare = hare.next.next

            #If hare catches up to tortoise then there is a loop
            if tortoise == hare:
                return True
            
        #If hare reaches the end of the list, then no loop is present
        return False



#Execution
#Add elements to the linked list and display them
new_list = LinkedList()
new_list.append("A")
new_list.append("B")
new_list.append("C")
new_list.append("D")
new_list.display() 

#Executions
new_list.insert_element_at_start("0")
new_list.display()
new_list.insert_after_element("C", "2")
new_list.display()
new_list.remove_first_occurrence("B")
new_list.display()
new_list.remove_item_at_num(4)
new_list.display()
new_list.check_if_element_exists("C")
new_list.display()
new_list.reverse()
new_list.display()
print (new_list.find_middle())
print (new_list.check_loop())
