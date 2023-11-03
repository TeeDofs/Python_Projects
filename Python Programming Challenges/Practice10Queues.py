#PRACTICE FOR QUEUES

class Queue:
    def __init__(self):
        self.queue = []

    #Add an item at the end of the queue
    def enqueue(self, item):
        self.queue.append(item)

    #Remove and return the item from the front of the queue
    def dequeue(self):
        if self.is_empty():
            return "Empty Queue!"
        return self.queue.pop(0)
    
    #Look at the front item without removal
    def peek(self):
        if self.is_empty():
            return "Empty Queue!"
        return self.queue[0]
    
    #Check if queue is empty
    def is_empty(self):
        return len(self.queue) == 0
    
    #Get the number of items in the queue
    def size(self):
        return len(self.queue)

class CircularQueue():
    def __init__(self, maxSize):
        self.queue = []
        self.maxSize = maxSize

    def enqueue(self, item):
        if self.size == self.maxSize:
            return "Queue already full !!!"
        self.queue.append(item)
    
    def dequeue(self):
        if self.is_empty():
            return "Queue is empty !!!"
        return self.queue.pop(0)
    
    def peek(self):
        if self.is_empty():
            return "Queue is empty !!!"
        return self.queue[0]
    
    def is_empty(self):
        return len(self.queue) == 0
    
    def size(self):
        return len(self.queue)
    
class GameLobby():
    def __init__(self):
        self.queue = []

    def enqueue(self, item, premium):
        self.queue.append((item, premium))

    def dequeue(self):
        for index, item in enumerate(self.queue):
            if item[1] == True:
                return self.queue.pop(index)[0]
        return self.queue.pop(0)[0]
    
    def peek(self):
        for item in self.queue:
            if item[1] == True:
                return item[0]
        return self.queue[0][0]



#Functions
def perform_operations(commands):
    queue = Queue()
    output = []

    for command in commands:
        if(len(command) == 2):
            #Do 2 operation
            if(command[0] == "enqueue"):
                queue.enqueue(command[1])
                output.append("None")
            else:
                return("this command is not valid")
        elif(len(command) == 1):
            #Do operation
            if(command[0] == "dequeue"):
                output.append(queue.dequeue())
            elif(command[0] == "peek"):
                output.append(queue.peek())
            else:
                return("this command is not valid")
        else:
            return("There is a problem with the list of commands")
   
    return output

def hot_potato(names, num):
    queue = Queue()

    for name in names:
        queue.enqueue(name)
    
    while queue.size() > 1:
        for _ in range(num - 1):
            queue.enqueue(queue.dequeue())
        
        queue.dequeue()
    return queue.peek()

#Executions
#Perform operations
# commands = [("enqueue", 1), ("enqueue", 2), ("peek",), ("dequeue",), ("peek",)]
# print(perform_operations(commands))

#Circular queue
# cq = CircularQueue(3)
# cq.enqueue(1)
# cq.enqueue(2)
# cq.enqueue(3)
# print(cq.enqueue(4))
# print(cq.dequeue())
# cq.enqueue(5)
# print(cq.peek())

#Game Lobby
# lobby = GameLobby()
# lobby.enqueue("player1", premium=False)
# lobby.enqueue("player2", premium=True)  # Premium player!
# lobby.enqueue("player3", premium=False)
# print(lobby.dequeue()) # player2
# print(lobby.dequeue()) # player1

#Hot Potato
name_list = ["Bill", "David", "Susan", "Jane", "Kent", "Brad"]
#PRACTICE FOR QUEUES

class Queue:
    def __init__(self):
        self.queue = []

    #Add an item at the end of the queue
    def enqueue(self, item):
        self.queue.append(item)

    #Remove and return the item from the front of the queue
    def dequeue(self):
        if self.is_empty():
            return "Empty Queue!"
        return self.queue.pop(0)
    
    #Look at the front item without removal
    def peek(self):
        if self.is_empty():
            return "Empty Queue!"
        return self.queue[0]
    
    #Check if queue is empty
    def is_empty(self):
        return len(self.queue) == 0
    
    #Get the number of items in the queue
    def size(self):
        return len(self.queue)

class CircularQueue():
    def __init__(self, maxSize):
        self.queue = []
        self.maxSize = maxSize

    def enqueue(self, item):
        if self.size == self.maxSize:
            return "Queue already full !!!"
        self.queue.append(item)
    
    def dequeue(self):
        if self.is_empty():
            return "Queue is empty !!!"
        return self.queue.pop(0)
    
    def peek(self):
        if self.is_empty():
            return "Queue is empty !!!"
        return self.queue[0]
    
    def is_empty(self):
        return len(self.queue) == 0
    
    def size(self):
        return len(self.queue)
    
class GameLobby():
    def __init__(self):
        self.queue = []

    def enqueue(self, item, premium):
        self.queue.append((item, premium))

    def dequeue(self):
        for index, item in enumerate(self.queue):
            if item[1] == True:
                return self.queue.pop(index)[0]
        return self.queue.pop(0)[0]
    
    def peek(self):
        for item in self.queue:
            if item[1] == True:
                return item[0]
        return self.queue[0][0]



#Functions
def perform_operations(commands):
    queue = Queue()
    output = []

    for command in commands:
        if(len(command) == 2):
            #Do 2 operation
            if(command[0] == "enqueue"):
                queue.enqueue(command[1])
                output.append("None")
            else:
                return("this command is not valid")
        elif(len(command) == 1):
            #Do operation
            if(command[0] == "dequeue"):
                output.append(queue.dequeue())
            elif(command[0] == "peek"):
                output.append(queue.peek())
            else:
                return("this command is not valid")
        else:
            return("There is a problem with the list of commands")
   
    return output

def hot_potato(names, num):
    print("In hot potato")
    queue = Queue()

    for name in names:
        queue.enqueue(name)
    
    while queue.size() > 1:
        for _ in range(num - 1):
            queue.enqueue(queue.dequeue())
        
        queue.dequeue()
    return queue.peek()

def is_palindrome(s):
    pal_queue = Queue()
    # Remove spaces, convert to lowercase, and filter out non-alphanumeric characters
    clean_s = ''.join(filter(str.isalnum, s)).lower()

    for l in clean_s:
        pal_queue.enqueue(l)

    while pal_queue.size() > 1:
        if pal_queue.dequeue() != pal_queue.queue.pop(pal_queue.size()-1):
            return False

    return True

#Executions

#Perform operations
commands = [("enqueue", 1), ("enqueue", 2), ("peek",), ("dequeue",), ("peek",)]
print(perform_operations(commands))
print("-----------------------")

#Circular queue
cq = CircularQueue(3)
cq.enqueue(1)
cq.enqueue(2)
cq.enqueue(3)
print(cq.enqueue(4))
print(cq.dequeue())
cq.enqueue(5)
print(cq.peek())
print("-----------------------")

#Game Lobby
lobby = GameLobby()
lobby.enqueue("player1", premium=False)
lobby.enqueue("player2", premium=True)  # Premium player!
lobby.enqueue("player3", premium=False)
print(lobby.dequeue()) # player2
print(lobby.dequeue()) # player1
print("-----------------------")

#Hot Potato
name_list = ["Bill", "David", "Susan", "Jane", "Kent", "Brad"]
print(hot_potato(name_list, 7))
print("-----------------------")

#Palindrome
print(is_palindrome("A man a plan a canal Panama")) 
print(is_palindrome("radar"))  
print(is_palindrome("hello"))  
print("-----------------------")