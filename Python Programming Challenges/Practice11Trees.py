#PRACTICE FOR TREES
class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if not self.root:
            self.root = Node(key)
        else:
            self._insert_recursive(self.root, key)

    def _insert_recursive(self, node, key):
        if key < node.val:
            if node.left is None:
                node.left = Node(key)
            else:
                self._insert_recursive(node.left, key)
        elif key > node.val:
            if node.right is None:
                node.right = Node(key)
            else:
                self._insert_recursive(node.right, key)

    def search(self, key):
        return self._search_recursive(self.root, key)
    
    def _search_recursive(self, node, key):
        if node is None:
            return False
        if key == node.val:
            return True
        if key < node.val:
            return self._search_recursive(node.left, key)
        return self._search_recursive(node.right, key)
    

#FUNCTIONS
def in_order_traversal(node):
    if not node:
        return[]
    
    left_values = in_order_traversal(node.left)
    right_values = in_order_traversal(node.right)

    return left_values + [node.val] + right_values

#EXECUTIONS

#Implementing a binary tree
tree = BinaryTree()
tree.insert(10)
tree.insert(5)
tree.insert(15)
tree.insert(2)
tree.insert(7)

assert tree.search(15) == True
assert tree.search(8) == False

#In order traversal
print(in_order_traversal(tree.root))

#Maximum depth of a binary tree
