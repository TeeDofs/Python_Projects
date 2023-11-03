#PRACTICE PROBLEM FOR STACKS

class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)
    
    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        else:
            return "Stack is empty!"
        
    def peek(self):
        if not self.is_empty():
            return self.stack[-1]
        else:
            return "Stack is empty!"
        
    def is_empty(self):
        return len(self.stack) == 0
    
    def display(self):
        return self.stack
    
    def is_balanced(self, expression):
        self.stack = [] 

        for char in expression:
            if char == '(':
                self.push(char)
            elif char == ')':
                if not self.stack:
                    return False
                self.pop()

        return self.is_empty()
    
    def reverse_string(self, string):
        self.stack = []

        for char in string:
            self.push(char)

        new_string = ""
        while not self.is_empty():
            new_string += self.pop()

        return new_string

#Needs more study and understanding    
def infix_to_postfix(expression):
    priority = {'+':1, '-':1, '*':2, '/':2, '^':3}

    stack = Stack()
    postfix = ""

    for char in expression:
        if char.isdigit():
            postfix += char
        elif char == "(":
            stack.push(char)
        elif char == ")":
            while not stack.is_empty() and stack.peek() != '(':
                postfix += stack.pop()
            stack.pop()
        else:
            while (not stack.is_empty() and priority[char] <= priority.get(stack.peek(), 0)):
                postfix += stack.pop()
            stack.push(char)

    while not stack.is_empty():
        postfix += stack.pop()

    return postfix

def sort_stack(input_stack):
        temp_stack = Stack()

        while not input_stack.is_empty():
            tmp = input_stack.pop()

            while not temp_stack.is_empty() and temp_stack.peek() < tmp:
                input_stack.push(temp_stack.pop())

            temp_stack.push(tmp)
            
        return temp_stack      

#Needs more understanding but better understood than the infix one
def evaluate_postfix(expression):
    stack = Stack()

    for char in expression.split():
        if char.isdigit():
            print("Digit found: ", int(char))
            stack.push(int(char))
        else:
            if stack.is_empty():
                return "Error in expression"
            b = stack.pop()

            if stack.is_empty():
                return "Error in expression"
            a = stack.pop()

            if char == '+':
                stack.push(a + b)
            elif char == '-':
                stack.push(a - b)
            elif char == '*':
                stack.push(a * b)
            elif char == '/':
                stack.push(a / b)
    return stack.peek()


stack = Stack()
print(stack.is_balanced("(())"))     # True
print(stack.is_balanced("((()))"))   # True
print(stack.is_balanced(")("))       #False

print (stack.reverse_string("HELLO"))

s = Stack()
arr = [5, 1, 3, 2, 4]
for i in arr:
    s.push(i)

sorted_stack = sort_stack(s)
print(sorted_stack.display())
print(infix_to_postfix("3+4*2"))
print(evaluate_postfix("342*+"))
print(evaluate_postfix("45+2*"))